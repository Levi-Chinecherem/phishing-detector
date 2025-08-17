from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pickle
from src.feature_extraction import extract_features_from_url
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = None
OPTIMAL_THRESHOLD = 0.4  # Set based on typical ROC analysis; adjust after checking results/roc_curve.png

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
    proba = model.predict_proba(features)[0]
    prediction = 1 if proba[1] >= OPTIMAL_THRESHOLD else 0  # 0: Phishing, 1: Legitimate
    result = "Legitimate" if prediction == 1 else "Phishing"
    confidence = proba[1] if prediction == 1 else proba[0]
    confidence_str = f"{confidence * 100:.2f}%"
    features_dict = features.iloc[0].to_dict()
    return templates.TemplateResponse("result.html", {
        "request": request,
        "url": url,
        "result": result,
        "confidence": confidence_str,
        "features": features_dict
    })