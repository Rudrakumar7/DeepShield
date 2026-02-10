import re

def get_bot_response(user_message):
    """
    Returns a rule-based response for the chatbot.
    """
    msg = user_message.lower()

    # 1. Greetings & General
    if any(x in msg for x in ['hi', 'hello', 'hey', 'start']):
        return "Hello! I'm the DeepShield Assistant. How can I help you secure your digital life today?"
    
    if 'who are you' in msg:
        return "I am DeepShield, your AI-powered cybersecurity companion. I can help you detect deepfakes, check passwords, and avoid phishing."

    # 2. Tool-Specific Help
    if any(x in msg for x in ['phish', 'link', 'url', 'scam site']):
        return "You can check suspicious links using our **Phishing URL Checker**. Go to <a href='/tools/phishing-checker'>Security Tools</a> to scan a URL."

    if any(x in msg for x in ['password', 'strength', 'weak']):
        return "Password security is key! Use our <a href='/tools/password-strength'>Password Strength Checker</a> to test your current password, or generate a new one."

    if any(x in msg for x in ['generate', 'create password', 'new password']):
        return "Need a strong password? tailored to you? Try our <a href='/tools/password-generator'>Personalized Password Generator</a>."

    if any(x in msg for x in ['audio', 'voice', 'sound']):
        return "To detect AI-generated audio, upload your file to our <a href='/detect/audio'>Audio Detection</a> tool. We analyze spectral features to find anomalies."

    if any(x in msg for x in ['video', 'clip', 'face']):
        return "Our <a href='/detect/video'>Video Scanner</a> checks for deepfake artifacts frame-by-frame. Upload a clip to get started."

    if any(x in msg for x in ['image', 'photo', 'picture']):
        return "Suspect a fake image? Use our <a href='/detect/image'>Image Detection</a> tool to perform Error Level Analysis (ELA)."

    # 3. Educational / Cyber News
    if any(x in msg for x in ['news', 'latest', 'hack', 'breach']):
        return "Stay updated! Check out the <a href='/news'>Cyber News</a> feed for the latest security updates."

    if 'deepfake' in msg:
        return "Deepfakes are AI-generated media that swap faces or clone voices. DeepShield uses advanced analysis to spot the tiny imperfections they leave behind."

    # 4. Fallback
    return "I'm not sure about that. Try navigating to our **Dashboard** to explore all tools, or ask me about 'phishing', 'passwords', or 'audio detection'."
