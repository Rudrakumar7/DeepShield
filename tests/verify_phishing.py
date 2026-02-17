import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.phishing import check_url

def test_url(url, expected_type):
    print(f"\nAnalyzing: {url}")
    result = check_url(url)
    print(f"Result: {result['result']} (Risk: {result['risk_level']})")
    print(f"Details: {result['details']}")
    
    # Basic assertion
    if expected_type == "Safe" and result['result'] == "Safe":
        print("✅ PASS: Correctly identified as Safe")
    elif expected_type == "Suspicious" and result['result'] in ["Suspicious", "Caution"]:
        print("✅ PASS: Correctly identified as Suspicious/Caution")
    else:
        print(f"❌ FAIL: Expected {expected_type}, got {result['result']}")

if __name__ == "__main__":
    print("--- Verifying XGBoost Phishing Detection ---")
    
    # 1. Safe URL
    test_url("https://www.google.com", "Safe")
    
    # 2. Suspicious URL (IP address)
    test_url("http://192.168.1.1/login", "Suspicious")
    
    # 3. Phishing-like URL (Keywords + Length)
    test_url("http://secure-login-account-update-verify-billing.com/signin?id=12345", "Suspicious")
    
    # 4. Legit Site
    test_url("https://github.com/Rudrakumar7/DeepShield", "Safe")
