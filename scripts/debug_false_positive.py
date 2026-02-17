import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.phishing import check_url

def analyze():
    urls = [
        "https://tryhackme.com/challenges",
        "https://www.hackthebox.com",
        "https://portswigger.net",
        "https://pentesterlab.com"
    ]
    
    print("--- Analyzing Cybersecurity Training Sites ---\n")
    
    for url in urls:
        print(f"Testing: {url}")
        result = check_url(url)
        print(f"  Result: {result['result']} (Score: {result['risk_score']})")
        if result['result'] != "Safe":
            print(f"  Details: {result['details']}")
        print("-" * 30)

if __name__ == "__main__":
    analyze()
