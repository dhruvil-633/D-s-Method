import feedparser
from datetime import datetime, timezone

RSS_FEEDS = {
    "company": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=NVDA&region=US&lang=en-US",
    "market":  "https://feeds.finance.yahoo.com/rss/2.0/headline?s=XLK&region=US&lang=en-US",
    "index":   "https://feeds.finance.yahoo.com/rss/2.0/headline?s=QQQ&region=US&lang=en-US"
}

def fetch_rss(channel):
    feed = feedparser.parse(RSS_FEEDS[channel])
    articles = []

    for entry in feed.entries:
        articles.append({
            "time": datetime(*entry.published_parsed[:6], tzinfo=timezone.utc),
            "text": entry.get("title", "") + " " + entry.get("summary", "")
        })

    return articles
