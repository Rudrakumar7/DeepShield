import unittest
from utils.password_utils import (
    generate_random_password, 
    generate_passphrase, 
    generate_personalized_password,
    calculate_entropy,
    check_rate_limit,
    secure_shuffle
)
import string
import secrets
import time

class TestSecurePasswordGenerator(unittest.TestCase):

    def test_random_password_entropy(self):
        pwd = generate_random_password(length=20)
        entropy = calculate_entropy(pwd)
        print(f"Random Password: {pwd}, Entropy: {entropy}")
        self.assertGreater(entropy, 80) # Should be very strong

    def test_personalized_security(self):
        # Ensure it doesn't contain full name "Rudra"
        pwd = generate_personalized_password("Rudra", "2026", "SecureKey")
        entropy = calculate_entropy(pwd)
        print(f"Personalized: {pwd}, Entropy: {entropy}")
        
        self.assertNotIn("Rudra", pwd) 
        self.assertNotIn("SecureKey", pwd)
        self.assertGreater(entropy, 60) # Enforced min entropy
        self.assertGreaterEqual(len(pwd), 12)

    def test_passphrase_strength(self):
        pwd = generate_passphrase(num_words=5, separator=' ')
        print(f"Passphrase: {pwd}")
        words = pwd.split(' ')
        self.assertEqual(len(words), 5)

    def test_rate_limit(self):
        client = "test_client_1"
        allowed_count = 0
        for _ in range(30):
            if check_rate_limit(client):
                allowed_count += 1
        
        # Max is 20
        self.assertEqual(allowed_count, 20)
        self.assertFalse(check_rate_limit(client))

    def test_secure_shuffle(self):
        original = list(range(100))
        shuffled = original.copy()
        secure_shuffle(shuffled)
        self.assertNotEqual(original, shuffled)
        self.assertEqual(sorted(original), sorted(shuffled))

if __name__ == '__main__':
    with open('security_test_result.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f)
        unittest.main(testRunner=runner)
