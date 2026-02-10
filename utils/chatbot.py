import re
import os
import google.generativeai as genai
from flask import current_app
from flask_login import current_user
from utils.db import db
from utils.models import ChatHistory

def get_chat_history(user_id, limit=10):
    """
    Fetches and formats the last 'limit' interactions for the user.
    """
    try:
        # Fetch recent history (descending), then reverse to chronological
        history_items = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
        history_items = history_items[::-1] 
        
        formatted = []
        for h in history_items:
            formatted.append({'role': 'user', 'parts': [h.user_message]})
            formatted.append({'role': 'model', 'parts': [h.bot_response]})
        return formatted
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

def get_ai_response(user_message):
    """
    Queries Google Gemini API using persistent chat history.
    """
    api_key = current_app.config.get('GEMINI_API_KEY')
    
    if not api_key:
        return None  # Trigger fallback

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Load history if user is logged in
        history = []
        if current_user.is_authenticated:
            history = get_chat_history(current_user.id)
        
        # Start chat with history
        chat = model.start_chat(history=history)
        
        # System instruction is not directly supported in start_chat for all models/versions 
        # seamlessly as a 'system' role in history list for some versions. 
        # We'll prepend the system instruction to the current message or rely on the model's persona.
        # For simplicity and robustness, we'll just send the message. 
        # Ideally, we should set system_instruction on GenerativeModel init, but we are re-initing here.
        
        # Let's use the explicit system instruction if supported, or just prepend it contextually
        # if history is empty.
        
        if not history:
            system_prompt = (
                "You are DeepShield, an advanced AI cybersecurity assistant. "
                "Your goal is to help users protect themselves from digital threats. "
                "Be concise, professional, and helpful. "
            )
            response = chat.send_message(f"{system_prompt}\n\nUser: {user_message}")
        else:
            response = chat.send_message(user_message)
            
        text_response = response.text

        # Save interaction to DB
        if current_user.is_authenticated:
            try:
                new_chat = ChatHistory(
                    user_id=current_user.id, 
                    user_message=user_message, 
                    bot_response=text_response
                )
                db.session.add(new_chat)
                db.session.commit()
            except Exception as e:
                print(f"Error saving chat history: {e}")

        return text_response
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def get_rule_based_response(user_message):
    """
    Fallback rule-based response.
    """
    msg = user_message.lower()

    # 1. Greetings & General
    if any(x in msg for x in ['hi', 'hello', 'hey', 'start']):
        return "Hello! I'm the DeepShield Assistant. I can help with deepfake detection, password security, and phishing checks."
    
    if 'who are you' in msg:
        return "I am DeepShield, your AI-powered cybersecurity companion."

    # 2. Tool-Specific Help
    if any(x in msg for x in ['phish', 'link', 'url', 'scam']):
        return "To check suspicious links, use our <a href='/tools/phishing-checker'>Phishing URL Checker</a>."

    if any(x in msg for x in ['password']):
        return "Secure your accounts with our <a href='/tools/password-strength'>Password Tools</a>."

    if any(x in msg for x in ['deepfake', 'audio', 'video', 'image']):
        return "You can scan media for manipulation using our <a href='/detect/image'>Deepfake Detection Tools</a>."

    # 3. Fallback
    return "I am currently running in offline mode. Please add a Gemini API Key to enable my full AI capabilities, or ask me about 'passwords' or 'phishing'."

def get_bot_response(user_message):
    """
    Main entry point. Tries AI first, then falls back to rules.
    """
    # Try AI response first
    ai_response = get_ai_response(user_message)
    if ai_response:
        return ai_response
        
    # Fallback to rules if API fails or is not configured
    return get_rule_based_response(user_message)
