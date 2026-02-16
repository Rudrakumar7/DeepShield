import feedparser
import requests
import re
import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# RSS Feeds for Cybersecurity News
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",  # The Hacker News
    "https://www.bleepingcomputer.com/feed/",       # Bleeping Computer
    "https://krebsonsecurity.com/feed/",            # Krebs on Security
    "https://threatpost.com/feed/",                 # Threatpost
    "https://www.darkreading.com/rss.xml",          # Dark Reading
]

# Cache Configuration
_news_cache = {
    'data': [],
    'timestamp': 0
}
CACHE_TTL = 300  # 5 minutes in seconds

# Threat Analysis Keywords
THREAT_KEYWORDS = {
    'critical': ['zero-day', 'ransomware', 'data breach', 'critical vulnerability', 'apt', 'exploit', 'unpatched'],
    'high': ['malware', 'phishing', 'dos', 'backdoor', 'spyware', 'trojan'],
    'medium': ['patch', 'update', 'policy', 'compliance', 'bug bounty']
}

CATEGORIES = {
    'Vulnerability': ['cve', 'vulnerability', 'exploit', 'patch', 'bug'],
    'Malware': ['malware', 'ransomware', 'virus', 'trojan', 'spyware', 'botnet'],
    'Data Breach': ['breach', 'leak', 'exposed', 'database', 'hacked', 'stolen'],
    'Cybercrime': ['fraud', 'scam', 'phishing', 'dark web', 'hacker', 'arrest'],
    'Policy': ['regulation', 'compliance', 'law', 'gdpr', 'white house', 'government'],
    'General Security': [] # Default
}

def clean_html(raw_html):
    """
    Removes HTML tags and unescapes entities from a string.
    """
    if not raw_html:
        return ""
    clean_text = re.sub(r'<[^>]+>', '', raw_html) # Remove tags
    clean_text = unescape(clean_text)             # Unescape HTML entities
    return clean_text.strip()

def parse_date(entry):
    """
    Parses published date from feed entry to datetime object.
    Returns datetime object or current time if parsing fails.
    """
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])
    return datetime.now()

def analyze_article(title, summary):
    """
    Analyzes article content to determine category, severity, and importance score.
    """
    text = (title + " " + summary).lower()
    
    # Determine Severity and Importance Score
    severity = 'Low'
    score = 20 # Base score
    
    for kw in THREAT_KEYWORDS['critical']:
        if kw in text:
            severity = 'Critical'
            score += 40
            break
    if severity == 'Low':
        for kw in THREAT_KEYWORDS['high']:
            if kw in text:
                severity = 'High'
                score += 25
                break
    if severity == 'Low':
        for kw in THREAT_KEYWORDS['medium']:
            if kw in text:
                severity = 'Medium'
                score += 10
                break

    # Determine Category
    category = 'General Security'
    for cat, keywords in CATEGORIES.items():
        if any(k in text for k in keywords):
            category = cat
            break # Assign first matching category priority
            
    return category, severity, min(100, score)

def fetch_single_feed(feed_url):
    """
    Fetches a single RSS feed with timeout and error handling.
    """
    headers = {
        'User-Agent': 'DeepShield-NewsAgent/1.0',
        'Cache-Control': 'no-cache'
    }
    try:
        # Use requests first for timeout control
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        if feed.bozo:
            logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")
        
        source_title = feed.feed.get('title', 'Cyber News')
        articles = []
        
        for entry in feed.entries[:5]: # Limit per feed
            title = entry.get('title', 'No Title')
            link = entry.get('link', '#')
            
            # Use summary or description
            raw_summary = entry.get('summary', entry.get('description', ''))
            clean_summary = clean_html(raw_summary)
            # Truncate
            short_summary = (clean_summary[:197] + '...') if len(clean_summary) > 200 else clean_summary
            
            published_dt = parse_date(entry)
            
            category, severity, importance = analyze_article(title, short_summary)
            
            articles.append({
                'title': title,
                'link': link,
                'published': published_dt.strftime("%a, %d %b %Y %H:%M"),
                'published_dt': published_dt, # For sorting
                'summary': short_summary,
                'source': source_title,
                'category': category,
                'severity': severity,
                'importance_score': importance
            })
            
        return articles
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching {feed_url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Error processing {feed_url}: {e}")
        return []

def get_cyber_news():
    """
    Fetches, aggregates, cleans, filters, and sorts cybersecurity news from multiple sources.
    Uses caching and multi-threading for performance.
    """
    global _news_cache
    
    # Check Cache
    if time.time() - _news_cache['timestamp'] < CACHE_TTL and _news_cache['data']:
        logger.info("Serving news from cache")
        return _news_cache['data']
        
    logger.info("Fetching fresh news feeds...")
    all_articles = []
    seen_links = set()
    
    # Fetch feeds in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_single_feed, url): url for url in RSS_FEEDS}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                articles = future.result()
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Thread failed for {url}: {e}")

    # Deduplicate and Sort
    unique_articles = []
    for art in all_articles:
        if art['link'] not in seen_links:
            unique_articles.append(art)
            seen_links.add(art['link'])
            
    # Sort by date (newest first), then by importance
    # Use importance as secondary sort key? No, date is primary for news.
    unique_articles.sort(key=lambda x: x['published_dt'], reverse=True)
    
    # Strip the datetime object before returning (not JSON serializable usually, though Flask handles it, safer to remove or stringify)
    final_output = []
    for art in unique_articles[:15]: # Limit global result
        art_copy = art.copy()
        del art_copy['published_dt'] # Remove non-serializable object
        final_output.append(art_copy)
        
    # Update Cache
    if final_output:
        _news_cache = {
            'data': final_output,
            'timestamp': time.time()
        }
    elif _news_cache['data']:
        # If fetch failed but we have stale cache, return stale cache?
        logger.warning("Fetch failed, serving stale cache.")
        return _news_cache['data']
    else:
        # Fallback if everything fails and cache is empty
        return get_mock_news()

    return final_output

def get_mock_news():
    """
    Returns mock data for fallback or testing.
    """
    return [
        {
            'title': 'Zero-Day Vulnerability Found in Popular Browser',
            'link': '#',
            'published': datetime.now().strftime("%a, %d %b %Y %H:%M"),
            'summary': 'Security researchers have identified a critical vulnerability allowing remote code execution...',
            'source': 'DeepShield News',
            'category': 'Vulnerability',
            'severity': 'Critical',
            'importance_score': 90
        },
        {
            'title': 'New Phishing Campaign Targets Banking Users',
            'link': '#',
            'published': datetime.now().strftime("%a, %d %b %Y %H:%M"),
            'summary': 'A sophisticated phishing campaign is using AI-generated emails to steal credentials...',
            'source': 'DeepShield News',
            'category': 'Cybercrime',
            'severity': 'High',
            'importance_score': 75
        }
    ]

# AI Summarizer Stub
def ai_summarize_article(article_text):
    """
    Placeholder for future AI summarization.
    """
    pass
