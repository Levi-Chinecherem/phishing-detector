import os
import requests
from scipy.io.arff import loadarff
import pandas as pd

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
    return df

def preprocess(df):
    features = [
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'HTTPS_token'
    ]
    X = df[features]
    y = df['Result']
    return X, y