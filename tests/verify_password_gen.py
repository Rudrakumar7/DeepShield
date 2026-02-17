import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app
from utils.password_utils import generate_random_password, generate_passphrase, generate_personalized_password
from utils.password_strength import check_password_strength
import string

class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        app.config['LOGIN_DISABLED'] = True
        self.app = app.test_client()
        self.app.testing = True

    def test_random_password(self):
        pwd = generate_random_password(length=20, use_upper=True, use_digits=True, use_symbols=True)
        self.assertEqual(len(pwd), 20)
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))
        self.assertTrue(any(c in string.punctuation for c in pwd))
        # print(f"Random Password: {pwd}") # Removed print to clean output

    def test_passphrase(self):
        pwd = generate_passphrase(num_words=3, separator='.', capitalize=True)
        parts = pwd.split('.')
        self.assertEqual(len(parts), 3)
        self.assertTrue(all(p[0].isupper() for p in parts))
        # print(f"Passphrase: {pwd}")

    def test_personalized(self):
        # We can't predict exact content due to shuffling and substring usage
        pwd = generate_personalized_password("Rudra", "2026", "Secure")
        
        # Check length is reasonable (>= 12 enforced)
        self.assertGreaterEqual(len(pwd), 12)
        
        # Check entropy is decent
        strength = check_password_strength(pwd)
        self.assertGreater(strength['entropy'], 50)

    def test_entropy(self):
        weak = "password123"
        strong = "C0rr3ct-H0rs3-B@tt3ry-St@pl3"
        
        strength_weak = check_password_strength(weak)
        strength_strong = check_password_strength(strong)
        
        # print(f"Weak Entropy: {strength_weak['entropy']}, Time: {strength_weak.get('crack_time')}")
        # print(f"Strong Entropy: {strength_strong['entropy']}, Time: {strength_strong.get('crack_time')}")
        
        self.assertTrue(strength_strong['entropy'] > strength_weak['entropy'])
        self.assertEqual(strength_strong['strength'], 'Very Strong')
        self.assertIn('crack_time', strength_strong)
        self.assertNotEqual(strength_strong['crack_time'], 'Instantly')

    def test_api_random(self):
        response = self.app.post('/tools/password-generator', json={
            'type': 'random',
            'length': 12
        })
        data = response.get_json()
        self.assertIn('password', data)
        self.assertEqual(len(data['password']), 12)

if __name__ == '__main__':
    with open('result.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f)
        unittest.main(testRunner=runner)
