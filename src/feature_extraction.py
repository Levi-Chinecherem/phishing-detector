import pandas as pd
from urllib.parse import urlparse
import re

def extract_features_from_url(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname if parsed_url.hostname else ''
    features = {}

    # having_IP_Address
    try:
        features['having_IP_Address'] = -1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 1
    except:
        features['having_IP_Address'] = 1

    # URL_Length
    url_len = len(url)
    if url_len < 54:
        features['URL_Length'] = 1
    elif url_len < 76:
        features['URL_Length'] = 0
    else:
        features['URL_Length'] = -1

    # Shortining_Service
    shortening_services = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly', 'adf.ly', 'bit.do', 'mcaf.ee', 'su.pr']
    features['Shortining_Service'] = -1 if hostname in shortening_services else 1

    # having_At_Symbol
    features['having_At_Symbol'] = -1 if '@' in url else 1

    # double_slash_redirecting
    features['double_slash_redirecting'] = -1 if url.find('//', 8) > -1 else 1

    # Prefix_Suffix
    features['Prefix_Suffix'] = -1 if '-' in hostname else 1

    # having_Sub_Domain
    dot_count = hostname.count('.')
    if dot_count <= 1:
        features['having_Sub_Domain'] = 1
    elif dot_count == 2:
        features['having_Sub_Domain'] = 0
    else:
        features['having_Sub_Domain'] = -1

    # SSLfinal_State (approximated for POC)
    features['SSLfinal_State'] = 1 if parsed_url.scheme == 'https' else -1

    # HTTPS_token
    features['HTTPS_token'] = -1 if 'https' in hostname.lower() else 1

    feature_list = [features[col] for col in [
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'HTTPS_token'
    ]]
    return pd.DataFrame([feature_list], columns=[
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'HTTPS_token'
    ])