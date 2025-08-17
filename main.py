from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle
from src.feature_extraction import extract_features_from_url
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = None

@app.on_event("startup")
async def startup_event():
    global model
    with open("models/random_forest_model.pkl", "rb") as f:
        model = pickle.load(f)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, url: str = Form(...)):
    features = extract_features_from_url(url)
    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    # Assuming model.classes_ = [-1, 1]
    if np.array_equal(model.classes_, np.array([-1, 1])):
        phishing_idx = 0
        legit_idx = 1
    else:
        phishing_idx = 1
        legit_idx = 0
    if prediction == 1:
        result = "Legitimate"
        confidence = proba[legit_idx]
    else:
        result = "Phishing"
        confidence = proba[phishing_idx]
    confidence_str = f"{confidence * 100:.2f}%"
    features_dict = features.iloc[0].to_dict()
    return templates.TemplateResponse("result.html", {
        "request": request,
        "url": url,
        "result": result,
        "confidence": confidence_str,
        "features": features_dict
    })