import re
import socket
from urllib.parse import urlparse

def check_url(url):
    """
    Analyzes a URL for phishing characteristics.
    Returns a dictionary with 'result', 'confidence', and 'details'.
    """
    score = 0
    details = []
    
    # 1. Check for IP address in URL
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    if re.search(ip_pattern, url):
        score += 30
        details.append("URL contains an IP address instead of a domain.")

    # 2. Check for suspicious keywords
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm']
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        score += 20
        details.append("URL contains suspicious keywords often used in phishing.")

    # 3. Check for excessive length
    if len(url) > 75:
        score += 10
        details.append("URL is unusually long.")

    # 4. Check for @ symbol (often used to obscure destination)
    if '@' in url:
        score += 25
        details.append("URL contains '@' symbol, which can be used to trick browsers.")

    parsed = urlparse(url)
    if parsed.scheme != 'https':
        score += 15
        details.append("URL is not using HTTPS.")

    # Determination
    if score > 40:
        result = "Suspicious"
        risk_level = "High"
    elif score > 20:
        result = "Caution"
        risk_level = "Medium"
    else:
        result = "Safe"
        risk_level = "Low"

    return {
        'result': result,
        'risk_score': score,
        'risk_level': risk_level,
        'details': details if details else ["No immediate threats detected."]
    }
