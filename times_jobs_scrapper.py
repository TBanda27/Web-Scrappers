from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import pandas as pd


def get_times_jobs_url(job_title, location):
    """Build TimesJobs search URL from user input"""
    base_url = "https://m.timesjobs.com/mobile/jobs-search-result.html"

    # URL encode inputs
    encoded_job = quote_plus(job_title)
    encoded_location = quote_plus(location)

    # Build URL
    search_url = f"{base_url}?txtKeywords={encoded_job}&cboWorkExp1=-1&txtLocation={encoded_location}"
    return search_url


def scrape_times_jobs(job_title, location):
    """Scrape TimesJobs based on search criteria"""

    # Build URL
    search_url = get_times_jobs_url(job_title, location)
    print(f"\nSearching for: {job_title} in {location}")
    print(f"URL: {search_url}\n")

    # Start browser
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(search_url)
    time.sleep(5)

    print("Auto-scrolling to load all jobs...\n")

    all_jobs_data = []
    seen_job_urls = set()
    body = driver.find_element(By.TAG_NAME, 'body')

    scroll_count = 0
    consecutive_no_new_jobs = 0
    max_consecutive_no_new = 5

    while True:
        scroll_count += 1
        print(f"Scroll {scroll_count}:")

        # Scroll
        for _ in range(3):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
        time.sleep(2)

        # Parse page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_list = soup.find('ul', id='jobsListULid')  # Replace
        job_items = job_list.find_all('li') if job_list else []

        print(f"  Total jobs in DOM: {len(job_items)}")

        new_jobs_this_scroll = 0

        for job in job_items:
            try:
                job_title_link = job.find('h3')
                if job_title_link:
                    job_title_link = job_title_link.find('a')
                if not job_title_link:
                    continue

                job_url = job_title_link.get('href', '')
                if not job_url or job_url in seen_job_urls:
                    continue

                seen_job_urls.add(job_url)

                title_text = job_title_link.text.strip()
                company = job.find('span', class_='srp-comp-name')
                company_text = company.text.strip() if company else 'N/A'
                loc = job.find('div', class_='srp-loc')
                location_text = loc.text.strip() if loc else 'N/A'
                experience = job.find('div', class_='srp-exp')
                exp_text = experience.text.strip() if experience else 'N/A'
                skills_div = job.find('div', class_='srp-keyskills')
                if skills_div:
                    skill_tags = skills_div.find_all('a', class_='srphglt')
                    skills_text = ', '.join([s.text.strip() for s in skill_tags])
                else:
                    skills_text = 'N/A'

                all_jobs_data.append({
                    'Title': title_text,
                    'Company': company_text,
                    'Location': location_text,
                    'Experience': exp_text,
                    'Skills': skills_text,
                    'URL': job_url
                })

                new_jobs_this_scroll += 1

            except Exception as e:
                continue

        print(f"  New jobs found: {new_jobs_this_scroll}")
        print(f"  Total unique jobs: {len(all_jobs_data)}")

        if new_jobs_this_scroll == 0:
            consecutive_no_new_jobs += 1
            print(f"  ⚠️  No new jobs ({consecutive_no_new_jobs}/{max_consecutive_no_new})")

            if consecutive_no_new_jobs >= max_consecutive_no_new:
                print(f"\n✓ Reached end!")
                break
        else:
            consecutive_no_new_jobs = 0
            print(f"  ✓ Still loading jobs...")

        print()

    driver.quit()

    print(f"\n{'=' * 70}")
    print(f"SCRAPING COMPLETE")
    print(f"{'=' * 70}")
    print(f"Total unique jobs scraped: {len(all_jobs_data)}")

    # Save to CSV
    filename = f"times_jobs_{job_title.replace(' ', '_')}_{location.replace(' ', '_')}.csv"
    df = pd.DataFrame(all_jobs_data)
    df.to_csv(filename, index=False)
    print(f"\n✓ Saved to {filename}")

    return all_jobs_data


if __name__ == "__main__":
    print("=" * 100)
    print("TimesJobs Scraper")
    print("=" * 100)

    job_title = input("\nEnter job title (e.g., Python Developer, Java): ")
    location = input("Enter location (e.g., Bangalore, Mumbai, leave blank for all): ")

    jobs = scrape_times_jobs(job_title, location)

    print(f"\nFirst 5 jobs:")
    for i, job in enumerate(jobs[:5], 1):
        print(f"{i}. {job['Title']} - {job['Company']} ({job['Location']})")
