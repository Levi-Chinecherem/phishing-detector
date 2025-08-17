# Phishing Detector MVP

This is a proof-of-concept Minimum Viable Product for detecting phishing websites using a Random Forest classifier. It uses a subset of features from the UCI Phishing Websites Dataset. The system includes data preprocessing, model training, and a FastAPI web app with Jinja2 templates for user interaction.

## Installation
1. Create a virtual environment (optional): `python -m venv env` and activate it.
2. Install dependencies: `pip install -r requirements.txt`

## How to train the model
Run: `python src/train_model.py`
- This will automatically download the dataset if not present, preprocess it, train the Random Forest model, evaluate it, and save the model to `models/random_forest_model.pkl`.

## How to start FastAPI server with uvicorn
Run: `uvicorn main:app --reload`
- Access the app at http://127.0.0.1:8000/

## Example prediction steps via the HTML form
1. Open http://127.0.0.1:8000/ in your browser.
2. Enter a URL (e.g., https://www.google.com).
3. Click "Check".
4. View the result: the URL and classification (Phishing or Legitimate).

## Dataset
The "Phishing Websites Dataset" from UCI is used. It contains pre-extracted features from URLs, with values -1 (suspicious), 0 (neutral), 1 (legitimate). The target is "Result" (1: legitimate, -1: phishing). No missing values; all features are integer-encoded.

## Data Preprocessing
- Loaded with Pandas.
- Selected subset of features that can be extracted from URL string.
- No scaling or encoding needed for Random Forest.

## Feature Engineering
The dataset contains URL-based features. For this MVP, a subset is used:
- having_IP_Address: -1 if hostname is IP, 1 otherwise.
- URL_Length: 1 if <54 chars, 0 if 54-75, -1 if >75.
- Shortining_Service: -1 if domain is a known shortener, 1 otherwise.
- having_At_Symbol: -1 if '@' present, 1 otherwise.
- double_slash_redirecting: -1 if '//' appears after protocol, 1 otherwise.
- Prefix_Suffix: -1 if '-' in hostname, 1 otherwise.
- having_Sub_Domain: 1 if ≤1 dots in hostname, 0 if 2, -1 if >2.
- SSLfinal_State: Approximated as 1 if HTTPS, -1 otherwise (note: full feature requires certificate details, simplified for POC).
- HTTPS_token: -1 if 'https' in hostname, 1 otherwise.

The `extract_features_from_url(url)` function in `feature_extraction.py` computes these for prediction.

## Model
Random Forest Classifier from scikit-learn. Evaluated with accuracy, precision, recall, F1, confusion matrix on 20% test split.

## Notes
- This is a POC; in production, extract more features (e.g., via WHOIS, page content) and use full dataset features.
- SSLfinal_State is approximated; real implementation needs certificate validation.
- No suspicious keywords feature added as it's not in the dataset, but can be extended.