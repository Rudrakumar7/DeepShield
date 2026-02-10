import random
import string

def leet_speak(text):
    subs = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
    return "".join(subs.get(c.lower(), c) for c in text)

def generate_personalized_password(name, year, keyword, include_symbols=True):
    """
    Generates a password based on user details.
    """
    if not name: name = "User"
    if not year: year = "2024"
    if not keyword: keyword = "Secure"

    # Strategy 1: Interleaved with special chars
    parts = [name.capitalize(), keyword.capitalize()]
    random.shuffle(parts)
    
    base = parts[0] + parts[1]
    
    # Apply leet speak to half of the base or randomly
    if random.choice([True, False]):
        base = leet_speak(base)
    
    # Add Year
    base += str(year)
    
    # Add Symbols
    if include_symbols:
        symbols = "!@#$%^&*"
        base = random.choice(symbols) + base + random.choice(symbols)
    
    # Ensure some randomness if it's too simple
    if len(base) < 12:
        base += "".join(random.choices(string.ascii_letters + string.digits, k=4))

    return base

def generate_random_password(length=12):
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return "".join(random.choice(charset) for _ in range(length))
