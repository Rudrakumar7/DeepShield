import re
from urllib.parse import urlparse
from utils.phishing_model import PhishingClassifier

# Initialize and load model once
classifier = PhishingClassifier()
model_loaded = classifier.load_model()

def check_url(url):
    """
    Analyzes a URL for phishing characteristics using XGBoost model.
    Falls back to heuristics if model is not available.
    """
    # 1. Run Heuristics First
    heuristic_score = 0
    heuristic_details = []
    
    # Check for IP address in URL
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    if re.search(ip_pattern, url):
        heuristic_score += 30
        heuristic_details.append("URL contains an IP address instead of a domain.")

    # Check for suspicious keywords (Cumulative Score)
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm', 'signin', 'wallet', 'alert']
    keyword_count = sum(1 for keyword in suspicious_keywords if keyword in url.lower())
    if keyword_count > 0:
        # +20 for the first keyword, +10 for each additional (cap at 50)
        heuristic_score += 20 + (keyword_count - 1) * 10
        heuristic_score = min(heuristic_score, 70) # Cap keyword score contribution
        heuristic_details.append(f"URL contains {keyword_count} suspicious keywords (e.g., '{next(k for k in suspicious_keywords if k in url.lower())}').")

    # Check for excessive length
    if len(url) > 75:
        heuristic_score += 10
        heuristic_details.append("URL is unusually long.")

    # Check for @ symbol
    if '@' in url:
        heuristic_score += 25
        heuristic_details.append("URL contains '@' symbol, attempting to obscure destination.")

    parsed = urlparse(url)
    if parsed.scheme != 'https':
        heuristic_score += 15
        heuristic_details.append("URL is not using HTTPS.")

    # 2. Run AI Model
    ml_confidence = 0.0
    ml_result = "Unknown"
    ml_details = []
    
    if model_loaded:
        prob_phishing = classifier.predict(url)
        if prob_phishing is not None:
            is_phishing = prob_phishing > 0.5
            ml_confidence = prob_phishing * 100 if is_phishing else (1 - prob_phishing) * 100
            
            if is_phishing:
                ml_result = "Suspicious"
                ml_details.append(f"AI Model detected phishing patterns (Confidence: {ml_confidence:.2f}%).")
            else:
                ml_result = "Safe"
                ml_details.append(f"AI Model analyzed URL as legitimate (Confidence: {ml_confidence:.2f}%).")

    # 3. Hybrid Decision Logic
    final_result = "Safe"
    final_risk_level = "Low"
    final_details = []
    final_score = 0

    # Trust Whitelist (Overrides everything else for Root Domains)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    if domain.startswith('www.'):
        domain = domain[4:]
    trusted_domains = ['github.com', 'google.com', 'microsoft.com', 'gitlab.com', 'stackoverflow.com', 'amazon.com']
    
    is_trusted_domain = any(d == domain for d in trusted_domains)
    
    if is_trusted_domain:
        # Check for suspicious file extensions in path
        suspicious_exts = ['.exe', '.zip', '.rar', '.scr', '.bat', '.sh', '.bin']
        path_lower = parsed_url.path.lower()
        if any(path_lower.endswith(ext) for ext in suspicious_exts):
             # Trusted domain but serving executable -> Caution
             final_result = "Caution"
             final_risk_level = "Medium"
             final_details.append(f"Trusted domain {domain}, but URL links to an executable/archive file. Verify source.")
             return {
                'result': final_result,
                'risk_score': 50,
                'risk_level': final_risk_level,
                'details': final_details
            }
        
        # Otherwise, trust the domain
        final_result = "Safe"
        final_risk_level = "Low"
        final_details.append(f"Verified Safe: {domain} is a trusted platform.")
        return {
            'result': final_result,
            'risk_score': 0,
            'risk_level': final_risk_level,
            'details': final_details
        }

    # Combine Scores
    # Heuristic Score Range: 0 - 100
    # Model Score: 0 or 100 (weighted)
    
    if ml_result == "Suspicious":
        final_result = "Suspicious"
        final_risk_level = "High" if ml_confidence > 80 else "Medium"
        final_details.extend(ml_details)
        final_score = int(ml_confidence)
        
        # Add heuristic details if they confirm the suspicion
        if heuristic_score > 0:
            final_details.extend(heuristic_details)
            
    elif heuristic_score > 40:
        # Model said Safe, but Heuristics say Suspicious -> CAUTION
        final_result = "Suspicious" # Upgrade to Suspicious if strong heuristic signals (like IP)
        final_risk_level = "High"
        final_details.append("AI Model was unsure, but strong heuristic signals were detected.")
        final_details.extend(heuristic_details)
        final_score = heuristic_score
        
    elif heuristic_score > 20:
        # Model said Safe, but some heuristics present -> CAUTION
        final_result = "Caution"
        final_risk_level = "Medium"
        final_details.append("AI Model considers this Safe, but proceed with caution.")
        final_details.extend(heuristic_details)
        final_score = heuristic_score
        
    else:
        # Both say Safe
        final_result = "Safe"
        final_risk_level = "Low"
        final_details.extend(ml_details)
        final_score = int(ml_confidence) if model_loaded else 0

    return {
        'result': final_result,
        'risk_score': final_score,
        'risk_level': final_risk_level,
        'details': final_details if final_details else ["No immediate threats detected."]
    }
