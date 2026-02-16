import re
import math
from utils.password_utils import calculate_entropy, calculate_crack_time, get_strength_rating

def check_repetition(password):
    """
    Checks for:
    1. Consecutive repeated characters (e.g., 'aaaa').
    2. High repetition ratio (length vs unique chars).
    Returns penalty score and feedback.
    """
    penalty = 0
    feedback = set()
    
    # 1. Consecutive Repetition (3+ identical)
    if re.search(r'(.)\1\1', password):
        penalty += 10
        feedback.add("Reduce consecutive repeated characters (e.g., 'aaa').")
        
    # 2. Repetition Ratio
    if len(password) > 0:
        unique_chars = len(set(password))
        ratio = unique_chars / len(password)
        if ratio < 0.5:
            penalty += 15
            feedback.add("Use a wider variety of characters; too many repeats.")
            
    return penalty, list(feedback)

def check_sequential(password):
    """
    Checks for sequential characters (e.g., 'abc', '123') and accumulates penalties.
    Returns penalty score and feedback.
    """
    penalty = 0
    feedback = set()
    
    sequences = [
        '1234567890', '0987654321',
        'abcdefghijklmnopqrstuvwxyz', 'zyxwvutsrqponmlkjihgfedcba',
        'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
    ]
    
    lower_pwd = password.lower()
    matches_found = 0
    
    for seq in sequences:
        for i in range(len(seq) - 2): # Check for 3-char sequences
            sub = seq[i:i+3]
            if sub in lower_pwd:
                matches_found += 1
                penalty += 10 # Cumulative penalty per match
                feedback.add("Avoid common sequences like 'abc' or '123'.")
                
    # Cap total sequence penalty to avoid zeroing out strong passwords entirely
    penalty = min(penalty, 40)
    
    return penalty, list(feedback)

def check_keyboard_patterns(password):
    """
    Checks for common keyboard patterns like '1q2w', 'qaz', 'wsx'.
    Returns penalty score and feedback.
    """
    penalty = 0
    feedback = set()
    
    # Common adjacent key patterns (simplified)
    patterns = [
        '1qaz', '2wsx', '3edc', '4rfv', '5tgb', '6yhn', '7ujm', '8ik,', '9ol.', '0p;/',
        'qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm', 'ik,', 'ol.', 'p;/',
        'zaq', 'xsw', 'cde', 'vfr', 'bgt', 'nhy', 'mju', ',ki', '.lo', '/;p',
        '1q2w', '3e4r', '5t6y', '7u8i', '9o0p'
    ]
    
    lower_pwd = password.lower()
    for pat in patterns:
        if pat in lower_pwd:
            penalty += 15
            feedback.add("Avoid keyboard patterns like 'qaz' or '1q2w'.")
            # Break after first major pattern match to avoid excessive penalty, or accumulate?
            # Let's accumulate once but break inner loop if multiple patterns are subsets
            
    return penalty, list(feedback)

def check_common_words(password):
    """
    Checks for common weak passwords and accumulates penalties.
    Returns penalty score and feedback.
    """
    penalty = 0
    feedback = set()
    
    common_words = [
        'password', 'admin', 'welcome', 'login', '123456', 'qwerty', 
        'football', 'monkey', 'dragon', 'master', 'freedom', 'computer',
        'superman', 'baseball', 'princess', 'jordan', 'shadow', 'secret',
        'love', 'hacker', 'orange', 'purple', 'starwars'
    ]
    
    lower_pwd = password.lower()
    for word in common_words:
        if word in lower_pwd:
            penalty += 20
            feedback.add(f"Avoid common words like '{word}'.")
            
    penalty = min(penalty, 60) # Cap at 60
    return penalty, list(feedback)

def check_complexity(password):
    """
    Checks if password lacks fundamental complexity types.
    Returns 0 (no penalty, just feedback) and feedback.
    """
    feedback = set()
    
    if password.isalpha():
        feedback.add("Add numbers and symbols for better security.")
    elif password.isdigit():
        feedback.add("Add letters and symbols. Numbers alone are weak.")
        
    return 0, list(feedback)

def check_breached_password(password):
    """
    Placeholder for breach detection (e.g., HaveIBeenPwned API).
    """
    # In a real impl, this would hash the password and check an API or local DB.
    # For now, it's a pass-through.
    return 0, []

def check_password_strength(password):
    """
    Evaluates the strength of a password using entropy and advanced heuristics.
    Returns a dict with score (0-100), entropy, strength level, feedback, and crack time.
    """
    feedback = set()
    
    if not password:
        return {'score': 0, 'entropy': 0, 'strength': 'Empty', 'feedback': ['Please enter a password.'], 'crack_time': 'N/A'}

    length = len(password)
    
    # 0. Max Length Check
    if length > 128:
        feedback.add("Password is very long. Consider using a password manager if you aren't already.")

    # 1. Base Entropy Calculation
    entropy = calculate_entropy(password)
    
    # 2. Heuristic Penalties
    penalties = 0
    
    # Repetition
    pen, fb = check_repetition(password)
    penalties += pen
    feedback.update(fb)
    
    # Sequential
    pen, fb = check_sequential(password)
    penalties += pen
    feedback.update(fb)
    
    # Keyboard Patterns
    pen, fb = check_keyboard_patterns(password)
    penalties += pen
    feedback.update(fb)
    
    # Common Words
    pen, fb = check_common_words(password)
    penalties += pen
    feedback.update(fb)
    
    # Complexity Warnings (No penalty, just advice)
    _, fb = check_complexity(password)
    feedback.update(fb)

    # Breached Check (Stub)
    _, fb = check_breached_password(password)
    feedback.update(fb)

    # 3. Apply Penalties
    final_entropy = max(0, entropy - penalties)

    # 4. Length Feedback (Advice)
    if length < 8:
        feedback.add("Password is too short (min 8 characters).")
        
    # 5. Complexity Breakdown (Advice - standard check)
    if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
        feedback.add("Mix uppercase and lowercase letters.")
    if not re.search(r"\d", password):
        feedback.add("Add numbers.")
    if not re.search(r"[^a-zA-Z0-9]", password):
        feedback.add("Add special characters (e.g. !@#$).")
        
    if not feedback:
        feedback.add("Excellent password! Looks strong.")

    # 6. Crack Time Calculation
    crack_time = calculate_crack_time(final_entropy)

    # 7. Scaled Scoring (0-100)
    # 80 bits = 100 score
    # Score = min(100, (entropy / 80) * 100)
    score = min(100, int((final_entropy / 80) * 100))
    
    # 8. Determine Strength Label
    strength = get_strength_rating(final_entropy)
    
    return {
        'score': score,
        'entropy': round(final_entropy, 2),
        'strength': strength,
        'crack_time': crack_time,
        'feedback': list(feedback)
    }
