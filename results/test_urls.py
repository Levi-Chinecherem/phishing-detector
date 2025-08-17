import pandas as pd
import pickle
import os
from feature_extraction import extract_features_from_url
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Test URLs
test_urls = [
    'http://paypa1.com/login',
    'http://secure-netflix-billing.com/account',
    'http://amaz0n-support.net/reset',
    'http://bankofamerica-login.secure-access.xyz/account',
    'http://g00gle.com@malicious-site.info',
    'http://tinyurl.com.redirect@phish-site.com',
    'http://192.168.1.1.login-page.com',
    'http://microsoft-security-alert.com//update',
    'http://login-secure.com/https/amazon',
    'http://apple-support-1234567890.com/repair',
    'https://www.google.com',
    'https://www.paypal.com'
]

# Load model
with open('models/random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Test each URL
results = []
OPTIMAL_THRESHOLD = 0.4  # Match main.py
for url in test_urls:
    logger.debug(f"\nTesting URL: {url}")
    features = extract_features_from_url(url)
    proba = model.predict_proba(features)[0]
    prediction = 1 if proba[1] >= OPTIMAL_THRESHOLD else 0
    result = "Legitimate" if prediction == 1 else "Phishing"
    confidence = proba[1] if prediction == 1 else proba[0]
    feature_dict = features.iloc[0].to_dict()
    feature_dict['URL'] = url
    feature_dict['Result'] = result
    feature_dict['Confidence'] = f"{confidence * 100:.2f}%"
    results.append(feature_dict)
    logger.debug(f"Prediction: {result}, Confidence: {confidence * 100:.2f}%")

# Save results
results_dir = 'results/'
os.makedirs(results_dir, exist_ok=True)
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(results_dir, 'test_urls.csv'), index=False)
logger.debug(f"Test results saved to {results_dir}test_urls.csv")