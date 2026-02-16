import secrets
import string
import os
import math
import time
import re

# Rate Limiting Storage (Simple In-Memory)
# Format: {ip_address: [timestamp, timestamp, ...]}
_request_history = {}
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 20

def check_rate_limit(client_id):
    """
    Checks if a client has exceeded the rate limit.
    Returns True if allowed, False if blocked.
    """
    now = time.time()
    history = _request_history.get(client_id, [])
    
    # Filter out old requests
    valid_requests = [t for t in history if now - t < RATE_LIMIT_WINDOW]
    
    if len(valid_requests) >= MAX_REQUESTS_PER_WINDOW:
        return False
    
    valid_requests.append(now)
    _request_history[client_id] = valid_requests
    return True

def secure_shuffle(items):
    """
    Shuffles a list using secrets.randbelow for cryptographic strength.
    Fisher-Yates shuffle algorithm.
    """
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]

def calculate_entropy(password):
    """
    Calculates the entropy of a password based on its character pool.
    """
    pool_size = 0
    if re.search(r"[a-z]", password):
        pool_size += 26
    if re.search(r"[A-Z]", password):
        pool_size += 26
    if re.search(r"\d", password):
        pool_size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool_size += 32  # Approximate for symbols
        
    if pool_size == 0:
        return 0
    
    entropy = len(password) * math.log2(pool_size)
    return entropy

def get_strength_rating(entropy):
    """
    Returns a strength rating based on entropy bits.
    """
    if entropy < 40:
        return "Weak"
    elif entropy < 60:
        return "Medium"
    elif entropy < 80:
        return "Strong"
    else:
        return "Very Strong"

def calculate_crack_time(entropy):
    """
    Estimates time to crack based on entropy, assuming 100 billion guesses per second (offline GPU array).
    """
    guesses = 2 ** entropy
    guesses_per_second = 100_000_000_000 # 100 Billion/sec (High-end GPU Cluster)
    
    seconds = guesses / guesses_per_second
    
    if seconds < 1:
        return "Instantly"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000:
        days = int(seconds // 86400)
        return f"{days} days"
    elif seconds < 3153600000:
        years = int(seconds // 31536000)
        return f"{years} years"
    else:
        return "Centuries"

def leet_speak(text):
    subs = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
    return "".join(subs.get(c.lower(), c) for c in text)

def load_wordlist():
    try:
        # Assuming wordlist.txt is in the same directory as this file
        file_path = os.path.join(os.path.dirname(__file__), 'wordlist.txt')
        with open(file_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
        
        # Security Warning for small wordlists
        if len(words) < 100:
            print("Warning: Wordlist is very small. Passphrases may be predictable.")
            
        return words
    except Exception:
        # Fallback list if file not found
        return ["apple", "brave", "cloud", "delta", "eagle", "flame", "giant", "house", "kite", "lemon"]

def generate_personalized_password(name, year, keyword, include_symbols=True, min_entropy=60):
    """
    Generates a secure password using substrings of user details mixed with secure random characters.
    Enforces a minimum entropy threshold.
    """
    if not name: name = "User"
    if not year: year = "2024"
    if not keyword: keyword = "Secure"

    # 1. Extract substrings to avoid full predictable words
    # Take first 2 chars or last 2, etc.
    p1 = name[:2].capitalize() if len(name) >= 2 else name.capitalize()
    p2 = keyword[:2].capitalize() if len(keyword) >= 2 else keyword.capitalize()
    p3 = str(year)[-2:] if len(str(year)) >= 2 else str(year)
    
    parts = [p1, p2, p3]
    
    # 2. Add cryptographically secure random core
    # Add 6 random characters to ensure base entropy
    core_charset = string.ascii_letters + string.digits + ("!@#$%^&*" if include_symbols else "")
    random_core = "".join(secrets.choice(core_charset) for _ in range(6))
    parts.append(random_core)

    # 3. Secure Shuffle
    secure_shuffle(parts)
    base = "".join(parts)
    
    # 4. Leet Speak (Optional randomization)
    if secrets.choice([True, False]):
        base = leet_speak(base)

    # 5. Dynamic Padding to minimum length (12)
    while len(base) < 12:
        base += secrets.choice(string.ascii_letters + string.digits)
        
    # 6. Secure Shuffle Final Characters to remove pattern of "chunks"
    # Convert to list, shuffle, join
    char_list = list(base)
    secure_shuffle(char_list)
    password = "".join(char_list)
    
    # 7. Entropy Check
    if calculate_entropy(password) < min_entropy:
        # If too weak (unlikely with random core), add more random chars
        password += "".join(secrets.choice(core_charset) for _ in range(4))
        
    return password

def generate_random_password(length=16, use_upper=True, use_digits=True, use_symbols=True, avoid_ambiguous=True):
    """
    Generates a cryptographically secure random password.
    """
    # Define character sets
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase if use_upper else ""
    digits = string.digits if use_digits else ""
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if use_symbols else ""
    
    if avoid_ambiguous:
        ambiguous = "1lI0O"
        for char in ambiguous:
            lower = lower.replace(char, "")
            upper = upper.replace(char, "")
            digits = digits.replace(char, "")

    charset = lower + upper + digits + symbols
    if not charset:
        charset = string.ascii_lowercase # Fallback

    # Ensure at least one character from each selected category
    password_chars = []
    if use_upper: password_chars.append(secrets.choice(upper))
    if use_digits: password_chars.append(secrets.choice(digits))
    if use_symbols: password_chars.append(secrets.choice(symbols))
    
    # Fill the rest
    remaining_length = length - len(password_chars)
    if remaining_length > 0:
        password_chars += [secrets.choice(charset) for _ in range(remaining_length)]
        
    # Shuffle the result securely
    secure_shuffle(password_chars)
    
    return "".join(password_chars)

def generate_passphrase(num_words=4, separator="-", capitalize=True):
    """
    Generates a passphrase from a wordlist.
    """
    words = load_wordlist()
    
    # Validation
    if len(words) < 50:
         # Fallback to random if wordlist is dangerously small
         return generate_random_password(length=20)

    selected_words = [secrets.choice(words) for _ in range(num_words)]
    
    if capitalize:
        selected_words = [w.capitalize() for w in selected_words]
        
    return separator.join(selected_words)
