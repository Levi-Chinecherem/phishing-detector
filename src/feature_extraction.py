import pandas as pd
from urllib.parse import urlparse
import re
import logging
from difflib import SequenceMatcher

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Known legitimate domains
LEGITIMATE_DOMAINS = [
    'paypal.com', 'netflix.com', 'amazon.com', 'bankofamerica.com',
    'google.com', 'microsoft.com', 'apple.com', 'facebook.com', 'twitter.com'
]

# Suspicious keywords
SUSPICIOUS_KEYWORDS = [
    'login', 'secure', 'account', 'billing', 'support', 'alert', 'verify', 'update',
    'security', 'password', 'reset', 'signin', 'auth'
]

def is_typosquatting(hostname, legitimate_domains):
    """Check if hostname is a typosquatting attempt."""
    if not hostname:
        return False
    hostname = hostname.lower()
    for legit_domain in legitimate_domains:
        similarity = SequenceMatcher(None, hostname, legit_domain).ratio()
        # High similarity (e.g., paypa1 vs paypal) or small edit distance
        if (similarity > 0.8 or sum(a != b for a, b in zip(hostname, legit_domain)) <= 2) and hostname != legit_domain:
            return True
    return False

def has_suspicious_keyword(url, hostname):
    """Check for suspicious keywords in URL or hostname."""
    url_lower = url.lower()
    hostname_lower = hostname.lower()
    return any(keyword in url_lower or keyword in hostname_lower for keyword in SUSPICIOUS_KEYWORDS)

def extract_features_from_url(url):
    url = url.strip().lower()
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname if parsed_url.hostname else parsed_url.path.split('@')[-1] if '@' in url else ''
    logger.debug(f"URL: {url}, Hostname: {hostname}")

    features = {}

    # having_IP_Address
    try:
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        features['having_IP_Address'] = -1 if hostname and re.match(ip_pattern, hostname.split('.')[0]) else 1
        logger.debug(f"having_IP_Address: {features['having_IP_Address']}")
    except:
        features['having_IP_Address'] = 1
        logger.debug("Exception in IP check, defaulting to 1")

    # URL_Length
    url_len = len(url)
    features['URL_Length'] = 1 if url_len < 54 else 0 if url_len < 76 else -1
    logger.debug(f"URL_Length: {features['URL_Length']} (length: {url_len})")

    # Shortining_Service
    shortening_services = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly', 'adf.ly', 'bit.do', 'mcaf.ee', 'su.pr']
    features['Shortining_Service'] = -1 if hostname and any(s in hostname for s in shortening_services) else 1
    logger.debug(f"Shortining_Service: {features['Shortining_Service']} (hostname: {hostname})")

    # having_At_Symbol
    features['having_At_Symbol'] = -1 if '@' in url else 1
    logger.debug(f"having_At_Symbol: {features['having_At_Symbol']}")

    # double_slash_redirecting
    features['double_slash_redirecting'] = -1 if '//' in url[7:] else 1
    logger.debug(f"double_slash_redirecting: {features['double_slash_redirecting']}")

    # Prefix_Suffix (includes typosquatting)
    features['Prefix_Suffix'] = -1 if hostname and ('-' in hostname or is_typosquatting(hostname, LEGITIMATE_DOMAINS)) else 1
    logger.debug(f"Prefix_Suffix: {features['Prefix_Suffix']} (typosquatting: {is_typosquatting(hostname, LEGITIMATE_DOMAINS)})")

    # having_Sub_Domain
    if hostname:
        parts = hostname.split('.')
        dot_count = len(parts) - 1  # Include TLD
        features['having_Sub_Domain'] = 1 if dot_count <= 1 else 0 if dot_count == 2 else -1
    else:
        features['having_Sub_Domain'] = -1
    logger.debug(f"having_Sub_Domain: {features['having_Sub_Domain']} (dot_count: {dot_count if hostname else 'N/A'})")

    # SSLfinal_State
    features['SSLfinal_State'] = 1 if parsed_url.scheme == 'https' else -1
    logger.debug(f"SSLfinal_State: {features['SSLfinal_State']} (scheme: {parsed_url.scheme})")

    # HTTPS_token
    features['HTTPS_token'] = -1 if hostname and 'https' in hostname else 1
    logger.debug(f"HTTPS_token: {features['HTTPS_token']}")

    # Suspicious_Keywords (new feature)
    features['Suspicious_Keywords'] = -1 if has_suspicious_keyword(url, hostname) else 1
    logger.debug(f"Suspicious_Keywords: {features['Suspicious_Keywords']}")

    feature_list = [features[col] for col in [
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'HTTPS_token', 'Suspicious_Keywords'
    ]]
    logger.debug(f"Feature Vector: {feature_list}")

    return pd.DataFrame([feature_list], columns=[
        'having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'SSLfinal_State', 'HTTPS_token', 'Suspicious_Keywords'
    ])