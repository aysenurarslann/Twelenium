# 🐦 Selenium-Based Twitter Scraper

This project is a tweet scraping tool built with Python and Selenium. It collects tweets containing specific keywords over a given date range and stores them in a local database and JSON format. The script is designed to work without the official Twitter API by mimicking user behavior via browser automation.

> ⚠️ Note: This project uses [X (formerly Twitter)](https://x.com) web search and may be affected by changes to the site's structure or anti-bot mechanisms.

---

## 📌 Features

- Keyword-based tweet collection
- Date-range filtering (day-by-day iteration)
- Turkish language support by default
- Extracts:
  - Tweet content
  - Timestamp (converted to Turkish time)
  - Username
  - Tweet URL and ID
  - Hashtags
  - Likes, retweets, comments
  - Image URLs (excluding profile pictures)
- Stores tweets in:
  - Local SQLite-like database
  - JSON export
- Skips and logs days with no tweet results
- Selenium automation with a persistent Chrome user profile

---


---

## 🚀 Usage

### ▶️ Run the script:

```bash
python main.py -s 2024-03-01 -e 2024-03-05 -l tr


