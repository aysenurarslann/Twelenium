# Twelenium |Twitter Data Collector

A Python-based web scraper built with Selenium to collect public Twitter data for academic and research purposes.

## 🎯 Purpose
- Collect tweets by keyword, date range, or user.
- Extract text content, likes, retweets, timestamps, and author info.
- Store results in structured formats: `SQLite` and `JSON`.
- Designed for **non-commercial, ethical research only**.

## ⚠️ Important Notes
- This tool does **not** collect private or sensitive user data.
- Respects `robots.txt` and avoids aggressive scraping.
- Uses delays between requests to prevent rate-limiting.
- Not intended for commercial use or mass data harvesting.

## 🛠️ Technologies Used
- Python
- Selenium
- BeautifulSoup (optional)
- SQLite / JSON
- Pandas (for analysis)

## 📂 Sample Output
```json
{
  "tweet_id": "123456789",
  "text": "Great day at the university!",
  "likes": 12,
  "retweets": 3,
  "timestamp": "2024-07-15T14:30:00Z",
  "author": "@user123"
}
