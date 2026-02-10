import feedparser
import requests
from datetime import datetime

# RSS Feeds for Cybersecurity News
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",  # The Hacker News
    "https://www.bleepingcomputer.com/feed/",       # Bleeping Computer
    "https://krebsonsecurity.com/feed/",            # Krebs on Security
]

def get_cyber_news():
    """
    Fetches the latest cybersecurity news from RSS feeds.
    Returns a list of dicts: {title, link, published, summary, source}
    """
    articles = []
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:5]: # Get top 5 from each
                # Clean up summary (sometimes contains HTML)
                summary = entry.get('summary', 'No summary available.')
                if '<' in summary:
                    # Simple regex to strip HTML tags if needed, or just truncate
                    pass 
                
                # Format Date
                published = entry.get('published', '')
                if not published:
                    published = datetime.now().strftime("%a, %d %b %Y")

                articles.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': published,
                    'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                    'source': feed.feed.get('title', 'Cyber News')
                })
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
            
    # Sort by published date if possible, but formats vary. 
    # For now, just shuffle or keep as is.
    return articles

# Fallback/Mock data if internet is down
def get_mock_news():
    return [
        {
            'title': 'Zero-Day Vulnerability Found in Popular Browser',
            'link': '#',
            'published': datetime.now().strftime("%a, %d %b %Y"),
            'summary': 'Security researchers have identified a critical vulnerability...',
            'source': 'DeepShield News'
        },
        {
            'title': 'New Phishing Campaign Targets Banking Users',
            'link': '#',
            'published': datetime.now().strftime("%a, %d %b %Y"),
            'summary': 'A sophisticated phishing campaign is using AI-generated emails...',
            'source': 'DeepShield News'
        }
    ]
