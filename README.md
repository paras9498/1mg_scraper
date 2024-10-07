# 1mg Scraper

A Python-based scraper to extract medicine details from the [1mg](https://www.1mg.com) website. This tool uses `cloudscraper` to bypass Cloudflare protection and saves the scraped data in an Excel file.

## Features

- Scrapes medicine details such as name, manufacturer, price, availability, etc.
- Handles Cloudflare protection using `cloudscraper`.
- Exports scraped data to Excel using `pandas` and appends data to existing files.
- Automatic retries for failed network requests.

## Requirements

- Python 3.x
- Required packages (install with `requirements.txt`):
  - cloudscraper
  - pandas
  - openpyxl

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/1mg-scraper.git
   cd 1mg-scraper
   ```
2. Install the required dependencies:

```pip install -r requirements.txt

```

3. Run the script to start scraping:

```python 1mg_scraper.py

```
