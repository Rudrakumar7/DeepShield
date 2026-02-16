import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.phishing import check_url

def reproduction():
    print("--- Reproduction Test: Altered URLs ---\n")
    
    test_cases = [
        # 1. Subdomain tricks (Should be Suspicious)
        ("https://google.com.security-check.xyz", "Suspicious"),
        ("https://www.paypal.com.confirmation-login.info", "Suspicious"),
        
        # 2. Typosquatting (Should be Suspicious)
        ("https://g00gle.com", "Suspicious"),
        ("https://faceb00k.com", "Suspicious"),
        ("https://paypa1.com", "Suspicious"),
        
        # 3. Path confusion (Should be Suspicious)
        ("https://www.google.com/url?q=http://malicious.com", "Suspicious"),
        
        # 4. Homograph attacks (Basic check)
        ("https://xn--80ak6aa92e.com", "Suspicious"), # apple.com in cyrillic (example)
        
        # 5. Hyphenated domains
        ("https://secure-google-login.com", "Suspicious"),
    ]

    for url, expected_type in test_cases:
        print(f"Testing: {url}")
        result = check_url(url)
        
        actual_result = result['result']
        actual_score = result['risk_score']
        details = result['details']
        
        print(f"  -> Prediction: {actual_result} (Score: {actual_score})")
        print(f"  -> Expected: {expected_type}")
        print(f"  -> Details: {details}\n")

if __name__ == "__main__":
    reproduction()
