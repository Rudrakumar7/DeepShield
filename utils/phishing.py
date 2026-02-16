import re
from urllib.parse import urlparse, parse_qs
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
    
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith('www.'):
        domain = domain[4:]

    # --- A. Homograph / Punycode Check ---
    if 'xn--' in domain:
        heuristic_score += 50
        heuristic_details.append(f"Suspicious Domain: Punycode usage detected ('{domain}'). Possible homograph attack.")

    # --- B. Typosquatting Check ---
    # Common targets: google, facebook, amazon, paypal, microsoft, apple, netflix
    # Common typos: 0 for o, 1 for l/i, rn for m, vv for w
    typo_patterns = [
        (r'g[0o]0gle', 'google'),
        (r'faceb[0o]0k', 'facebook'),
        (r'paypa[1l]', 'paypal'),
        (r'amaz[0o]n', 'amazon'),
        (r'micr[0o]s[0o]ft', 'microsoft'),
        (r'app[1l]e', 'apple'),
        (r'netf[1l]ix', 'netflix')
    ]
    
    for pattern, target in typo_patterns:
        # Check if pattern matches but IS NOT the target
        if re.search(pattern, domain) and target not in domain:
             heuristic_score += 40
             heuristic_details.append(f"Suspicious Domain: Potential typosquatting detected (resembles '{target}').")

    # --- C. IP Address Check ---
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    if re.search(ip_pattern, url):
        heuristic_score += 30
        heuristic_details.append("URL contains an IP address instead of a domain.")

    # --- D. Suspicious Keywords (Cumulative Score) ---
    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account', 'banking', 'confirm', 'signin', 'wallet', 'alert', 'bonus', 'free', 'giveaway']
    keyword_count = sum(1 for keyword in suspicious_keywords if keyword in url.lower())
    if keyword_count > 0:
        # +20 for the first keyword, +10 for each additional (cap at 50)
        score_add = 20 + (keyword_count - 1) * 10
        heuristic_score += min(score_add, 50)
        heuristic_details.append(f"URL contains {keyword_count} suspicious keywords.")

    # --- E. Excessive Length ---
    if len(url) > 75:
        heuristic_score += 10
        heuristic_details.append("URL is unusually long.")

    # --- F. Symbol Checks ---
    if '@' in url:
        heuristic_score += 25
        heuristic_details.append("URL contains '@' symbol, attempting to obscure destination.")

    if parsed.scheme != 'https':
        heuristic_score += 10
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

    # --- Trusted Whitelist with Safeguards ---
    trusted_domains = [
        'github.com', 'google.com', 'microsoft.com', 'gitlab.com', 'stackoverflow.com', 'amazon.com', 'wikipedia.org', 'nytimes.com',
        'tryhackme.com', 'hackthebox.com', 'portswigger.net', 'pentesterlab.com', 'offsec.com', 'ctftime.org'
    ]
    
    is_trusted_domain = any(domain == d or domain.endswith('.' + d) for d in trusted_domains)
    
    if is_trusted_domain:
        # Safeguard 1: Check for Open Redirects (e.g., google.com/url?q=http://malicious.com)
        query_params = parse_qs(parsed.query)
        has_redirect = False
        
        # Common redirect params
        redirect_keys = ['q', 'url', 'redirect', 'u', 'link', 'dest', 'target']
        for key in redirect_keys:
            if key in query_params:
                # If any param value looks like a URL (http), it's a redirect
                for val in query_params[key]:
                    if val.startswith('http'):
                        has_redirect = True
                        heuristic_score += 50 # Penalize open redirect
                        heuristic_details.append(f"Warning: Trusted domain '{domain}' is redirecting to an external URL ('{val[:30]}...').")
                        break
        
        # Safeguard 2: Check for File Extensions of Executables
        suspicious_exts = ['.exe', '.zip', '.rar', '.scr', '.bat', '.sh', '.bin']
        path_lower = parsed.path.lower()
        if any(path_lower.endswith(ext) for ext in suspicious_exts):
             heuristic_score += 30
             heuristic_details.append(f"Warning: Trusted domain '{domain}' linking to executable/archive.")
             has_redirect = True # Treat as suspicious

        if not has_redirect:
            # Verified Safe
            final_result = "Safe"
            final_details.append(f"Verified Safe: {domain} is a trusted platform.")
            return {
                'result': final_result,
                'risk_score': 0,
                'risk_level': "Low",
                'details': final_details
            }
        # If has_redirect, fall through to normal scoring logic below

    # Combine Scores
    
    # AI Override: If AI is very confident (>90%), it weighs heavily
    if ml_result == "Suspicious" and ml_confidence > 90:
        final_result = "Suspicious"
        final_risk_level = "High"
        final_details.extend(ml_details)
        final_score = int(ml_confidence)
        if heuristic_score > 0:
            final_details.extend(heuristic_details)

    # Heuristic Override: If Heuristic Score is high (>50), it is Suspicious regardless of AI
    elif heuristic_score > 50:
        final_result = "Suspicious"
        final_risk_level = "High"
        final_details.append("Strong heuristic signals detected.")
        final_details.extend(heuristic_details)
        if ml_result == "Suspicious":
             final_details.extend(ml_details)
        final_score = max(heuristic_score, int(ml_confidence) if ml_result=="Suspicious" else 0)

    # Caution Zone
    elif heuristic_score > 25 or ml_result == "Suspicious":
        final_result = "Caution"
        final_risk_level = "Medium"
        if ml_result == "Suspicious":
            final_details.extend(ml_details)
        if heuristic_score > 0:
            final_details.extend(heuristic_details)
        
        # Score is mix of both
        base_score = int(ml_confidence) if ml_result == "Suspicious" else 0
        final_score = max(base_score, heuristic_score)

    # Safe Zone
    else:
        final_result = "Safe"
        final_risk_level = "Low"
        final_details.extend(ml_details)
        # Low risk score for Safe
        final_score = int(100 - ml_confidence) if model_loaded else 0

    return {
        'result': final_result,
        'risk_score': min(final_score, 100),
        'risk_level': final_risk_level,
        'details': final_details if final_details else ["No immediate threats detected."]
    }
