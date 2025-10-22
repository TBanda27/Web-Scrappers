import daft_homes_all_dublin_scrapper
import schedule
import time
import pandas as pd
from datetime import datetime


def daily_scrape_job():
    """Daily scraping job"""
    print("=" * 50)
    print(f"Job started at {datetime.now()}")
    print("=" * 50)

    try:
        # Run scraper
        all_homes = daft_homes_all_dublin_scrapper.scrape_all_daft()

        # Save results
        if all_homes:
            df = pd.DataFrame(all_homes)
            df = df.drop_duplicates(subset=['Home_Url'], keep='first')

            timestamp = datetime.now().strftime('%Y-%m-%d')
            filename = f"daft_properties_{timestamp}.csv"
            df.to_csv(filename, index=False)

            print(f"\n✓ SUCCESS: Saved {len(df)} properties")
        else:
            print("\n⚠️ WARNING: No properties found")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

    print(f"Job completed at {datetime.now()}\n")


# Schedule for 10 PM daily
schedule.every().day.at("22:00").do(daily_scrape_job)

print("🕐 Scheduler is running...")
print("📅 Next run: Every day at 10:00 PM")
print("🛑 Press Ctrl+C to stop\n")

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)