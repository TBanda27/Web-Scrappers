@echo off
echo Starting Daft Scraper...
cd /d "D:\Python For Data Analytics\Web Scraping"
call ".venv\Scripts\activate"
python "D:\Python For Data Analytics\Web Scraping\daft_homes_all_dublin_scrapper.py"
echo Scraping complete!
pause