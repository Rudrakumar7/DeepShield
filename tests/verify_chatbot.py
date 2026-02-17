import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
from flask import Flask
from config import Config
from utils.chatbot import get_bot_response

# Mock App Context
app = Flask(__name__)
app.config.from_object(Config)

# Test Cases
print("--- Testing Chatbot Logic ---")

with app.app_context():
    # 1. Test Fallback (No Key or Mocked Failure)
    # We expect a fallback response if no key is present in env, or if we force it.
    print(f"Gemini Key Present: {bool(app.config.get('GEMINI_API_KEY'))}")
    
    response = get_bot_response("Hello")
    print(f"User: Hello\nBot: {response}\n")

    response = get_bot_response("password")
    print(f"User: password\nBot: {response}\n")
    
    # 2. Test Deepfake specific fallback
    response = get_bot_response("deepfake")
    print(f"User: deepfake\nBot: {response}\n")

print("--- Test Complete ---")
