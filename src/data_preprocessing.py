import os
import requests
from scipy.io.arff import loadarff
import pandas as pd
from feature_extraction import extract_features_from_url

def get_dataset():
    arff_path = 'data/phishing_dataset.arff'
    csv_path = 'data/phishing_dataset.csv'
    if not os.path.exists(csv_path):
        if not os.path.exists(arff_path):
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00327/Training%20Dataset.arff"
            r = requests.get(url)
            with open(arff_path, 'wb') as f:
                f.write(r.content)
        raw_data = loadarff(arff_path)
        df = pd.DataFrame(raw_data[0])
        df = df.astype(int)
        df.to_csv(csv_path, index=False)
    df = pd.read_csv(csv_path)
    
    # Expanded synthetic phishing URLs
    phishing_urls = [
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
        'http://faceb00k.com/signin',
        'http://tw1tter.com/verify',
        'http://login-paypal-secure.com/auth',
        'http://192.168.0.1.security-check.com',
        'http://g0ogle-search.com@phish.com',
        'http://netfl1x-billing.com/account-update',
        'http://secure-bankofamerica-login.xyz/password',
        'http://tiny.cc.redirect@malicious.com',
        'http://microsoft-account-recovery.com//reset',
        'http://appleid-login-987654.com/secure'
    ]
    synthetic_data = []
    for url in phishing_urls:
        features = extract_features_from_url(url)
        features['Result'] = -1  # Phishing label
        synthetic_data.append(features)
    synthetic_df = pd.concat(synthetic_data, ignore_index=True)
    
    # Combine UCI dataset with synthetic data
    df = pd.concat([df, synthetic_df], ignore_index=True)
    return df

def preprocess(df):
    features = [
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'HTTPS_token', 'Suspicious_Keywords'
    ]
    X = df[features]
    y = df['Result']
    return X, y