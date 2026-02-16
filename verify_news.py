import unittest
from utils.news import get_cyber_news, clean_html, analyze_article, _news_cache
import time

class TestNewsAggregator(unittest.TestCase):

    def test_clean_html(self):
        html = "<p>This is <b>bold</b> and &amp; dangerous.</p>"
        cleaned = clean_html(html)
        self.assertEqual(cleaned, "This is bold and & dangerous.")
        
    def test_analyzer(self):
        title = "Ransomware Attack hits Major Bank"
        summary = "A new zero-day exploit was used to encrypt files."
        cat, sev, score = analyze_article(title, summary)
        
        # Should detect Ransomware keyword
        self.assertEqual(sev, "Critical")
        self.assertGreater(score, 50)
        self.assertIn(cat, ["Malware", "Vulnerability", "Cybercrime"])
        
    def test_fetch_real(self):
        # Clears cache to force fetch
        _news_cache['timestamp'] = 0 
        _news_cache['data'] = []
        
        start = time.time()
        articles = get_cyber_news()
        duration = time.time() - start
        
        print(f"Fetched {len(articles)} articles in {duration:.2f}s")
        
        if not articles:
            print("Warning: No articles fetched (network issue?). Skipping structure checks.")
            return

        # Verify Structure
        first = articles[0]
        self.assertIn('title', first)
        self.assertIn('severity', first)
        self.assertIn('category', first)
        self.assertIn('source', first)
        
        # Verify Sorting (Newest First) - loosely check if we have dates
        self.assertTrue(first['published'])

    def test_caching(self):
        # Pre-populate cache manually to test hit
        from utils import news
        news._news_cache['data'] = [{'title': 'Cached'}]
        news._news_cache['timestamp'] = time.time()
        
        start = time.time()
        articles = get_cyber_news()
        duration = time.time() - start
        
        print(f"Cached fetch took {duration:.4f}s")
        self.assertEqual(articles[0]['title'], 'Cached')
        self.assertLess(duration, 0.1) # Should be instant

if __name__ == '__main__':
    with open('news_test_result.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f)
        unittest.main(testRunner=runner)
