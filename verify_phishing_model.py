import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.phishing import check_url

def verify():
    print("--- Phishing Detection System Verification ---\n")
    
    test_cases = [
        # --- SAFE URLs ---
        ("https://www.google.com", "Safe"),
        ("https://github.com/rudrakumar7/DeepShield", "Safe"),
        ("https://stackoverflow.com/questions/12345/python-example", "Safe"),
        ("https://www.amazon.com/dp/B08N5KWB9H", "Safe"),
        ("https://www.wikipedia.org", "Safe"),
        
        # --- PHISHING / SUSPICIOUS URLs ---
        # 1. IP Address
        ("http://192.168.1.1/login.html", "Suspicious"),
        
        # 2. Suspicious Keywords
        ("http://secure-login-paypal.com.account-update.info/signin", "Suspicious"),
        
        # 3. Open Redirect (Whitelist Bypass)
        ("https://google.com/url?q=http://malicious.com", "Suspicious"),
        
        # 4. Homograph / Punycode
        ("https://xn--80ak6aa92e.com", "Suspicious"),
        
        # 5. Typosquatting
        ("https://faceb00k.com", "Suspicious"),
        ("https://g00gle.com", "Suspicious"),
        ("https://paypa1.com", "Suspicious")
    ]

    passed = 0
    total = len(test_cases)

    for url, expected_type in test_cases:
        print(f"Testing: {url}")
        result = check_url(url)
        
        # Result is a dict: {'result': 'Safe'/'Suspicious'/'Caution', ...}
        # We consider 'Caution' as a type of warning, but for this binary test:
        # If we expect Safe, it should be Safe.
        # If we expect Suspicious, 'Suspicious' or 'Caution' accepts.
        
        actual_result = result['result']
        actual_score = result['risk_score']
        
        is_pass = False
        if expected_type == "Safe" and actual_result == "Safe":
            is_pass = True
        elif expected_type == "Suspicious" and actual_result in ["Suspicious", "Caution"]:
            is_pass = True
            
        status = "PASS" if is_pass else "FAIL"
        if is_pass:
            passed += 1
            
        print(f"  -> Prediction: {actual_result} (Score: {actual_score})")
        print(f"  -> Expected: {expected_type}")
        print(f"  -> {status}\n")
        
    print("--------------------------------------------------")
    print(f"Test Summary: {passed}/{total} Passed")
    print("--------------------------------------------------")

if __name__ == "__main__":
    verify()
