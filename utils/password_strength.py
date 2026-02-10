import re

def check_password_strength(password):
    """
    Evaluates the strength of a password.
    Returns a dict with score (0-100), strength level, and feedback.
    """
    score = 0
    feedback = []
    
    if not password:
        return {'score': 0, 'strength': 'Empty', 'feedback': ['Please enter a password.']}

    # 1. Length Check
    length = len(password)
    if length < 8:
        feedback.append("Password is too short (min 8 characters).")
    elif length >= 12:
        score += 25
        feedback.append("Good length.")
    else:
        score += 10
        feedback.append("Decent length, but could be longer.")

    # 2. Complexity Check
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 20
    else:
        feedback.append("Mix uppercase and lowercase letters.")
        
    if re.search(r"\d", password):
        score += 20
    else:
        feedback.append("Add numbers.")
        
    if re.search(r"[ !@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        score += 25
    else:
        feedback.append("Add special characters (e.g. !@#$).")

    # 3. Common Pattern Check
    common_patterns = ['123', 'abc', 'password', 'qwerty', 'admin']
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 20
        feedback.append("Avoid common patterns like '123' or 'abc'.")

    # Final logic
    if length >= 8: # Base score for meeting min length
        score += 10

    # Cap score
    score = max(0, min(100, score))

    # Determine Strength Label
    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Moderate"
    elif score < 90:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        'score': score,
        'strength': strength,
        'feedback': feedback
    }
