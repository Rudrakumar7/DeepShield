import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from utils.password_strength import check_password_strength

class TestAdvancedPasswordStrength(unittest.TestCase):
    
    def test_keyboard_pattern(self):
        # "1qaz2wsx" -> Keyboard pattern penalty
        res = check_password_strength("1qaz2wsx")
        print(f"Testing '1qaz2wsx': Score={res['score']}, Feedback={res['feedback']}")
        self.assertTrue(any("keyboard" in f.lower() for f in res['feedback']))
        self.assertLess(res['score'], 60)

    def test_repetition_ratio(self):
        # "longpasswordlongpassword" -> High ratio penalty
        res = check_password_strength("longpasswordlongpassword")
        print(f"Testing Repetitive: Score={res['score']}, Feedback={res['feedback']}")
        self.assertTrue(any("variety" in f.lower() for f in res['feedback']))
        
    def test_complexity_warning(self):
        # "passwordpassword" -> Alpha only warning
        res = check_password_strength("correcthorsebatterystaple") # Strong but alpha only
        print(f"Testing Alpha Only: Score={res['score']}, Feedback={res['feedback']}")
        self.assertTrue(any("add numbers" in f.lower() for f in res['feedback']))

    def test_scaled_score(self):
        # 80 bits should be roughly 100
        # "Correct-Horse-Battery-Staple-99!" is very strong
        res = check_password_strength("Correct-Horse-Battery-Staple-99!")
        print(f"Testing Scaled Score: Entropy={res['entropy']}, Score={res['score']}")
        self.assertEqual(res['score'], 100)
        self.assertGreater(res['entropy'], 80)
        
    def test_cumulative_penalties(self):
        # "abc123qwerty" -> Multiple sequence penalties
        res = check_password_strength("abc123qwerty")
        print(f"Testing Cumulative: Score={res['score']}")
        # Should be very low due to multiple sequences
        self.assertLess(res['score'], 30)

if __name__ == '__main__':
    with open('advanced_strength_test_result.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f)
        unittest.main(testRunner=runner)
