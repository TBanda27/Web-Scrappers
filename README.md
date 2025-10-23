# Daft.ie Property Scraper

A Python web scraper that automatically collects rental property listings from Daft.ie across all of Ireland.

## Features

- Scrapes all rental properties from Daft.ie
- Removes duplicate listings automatically
- Saves data to timestamped CSV files
- Extracts property details: category, location, price, description, and URL
- Can be scheduled to run daily using Windows Task Scheduler

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download ChromeDriver matching your Chrome version from [here](https://chromedriver.chromium.org/)

## Usage

### Manual Run
```bash
python scraper.py
```

### Scheduled Daily Run (Windows)

1. Create `run_scraper.bat`:
```batch
@echo off
cd D:\path\to\your\project
call .venv\Scripts\activate
python scraper.py
pause
```

2. Set up Windows Task Scheduler:
   - Open Task Scheduler (`Win + R` → `taskschd.msc`)
   - Create Basic Task
   - Set trigger to Daily at 10:00 PM
   - Action: Start program → Browse to `run_scraper.bat`

## Output

Properties are saved to: `daft_properties_YYYY-MM-DD.csv`

CSV columns: Category, Location, Price, Description, Home_Url

## Notes

- Scraping takes 30-60 minutes for all Ireland listings
- Respects 2-second delay between pages
- Stops after 3 consecutive empty pages