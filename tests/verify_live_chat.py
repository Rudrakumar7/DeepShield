import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from config import Config
from utils.chatbot import get_bot_response

# Mock App Context
app = Flask(__name__)
app.config.from_object(Config)

# Test Cases
print("--- Testing Chatbot Logic with API Key ---")

with app.app_context():
    # 1. Test AI Response
    # If the key is valid, we should get a response that is NOT one of the hardcoded fallbacks.
    print(f"Gemini Key Configured: {bool(app.config.get('GEMINI_API_KEY'))}")
    
    user_msg = "How do I secure my home router?"
    response = get_bot_response(user_msg)
    print(f"User: {user_msg}\nBot: {response}\n")
    
    # Check if it's a fallback (simple check)
    if "offline mode" in response:
        print("RESULT: Fallback triggered (API Key might be invalid or quota exceeded).")
    else:
        print("RESULT: AI Response received!")

print("--- Test Complete ---")
