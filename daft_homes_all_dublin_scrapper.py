from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from datetime import datetime


def build_daft_url(page=1):
    """Build URL for all Ireland properties"""
    base_url = "https://www.daft.ie/property-for-rent/ireland"
    return f"{base_url}?page={page}"


def scrape_daft_page(driver, url, seen_urls):
    """Scrape a single page from Daft.ie"""
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    homes_html = soup.find('ul', class_='sc-798c155d-4 kmVnWY')

    if not homes_html:
        return []

    homes_items = homes_html.find_all('li')
    page_homes = []
    duplicates_found = 0

    for home in homes_items:
        try:
            # Get price (try two possible classes)
            price = home.find('p', class_='sc-af41020b-0 dqCzFn')
            if not price:
                price = home.find('p', class_='sc-af41020b-0 bfBSFC')

            category = home.find('p', class_='sc-af41020b-0 btpgrM')
            location = home.find('p', class_='sc-af41020b-0 dVPJAx')
            house_url_tag = home.find('a', class_='sc-798c155d-19 cDtUBM')

            # Skip if no category and location and price
            if not category and not location and not price:
                continue

            # Extract home URL
            home_url = house_url_tag['href'] if house_url_tag and house_url_tag.get('href') else None

            # Check for duplicates
            if not home_url:
                continue

            if home_url in seen_urls:
                duplicates_found += 1
                continue

            seen_urls.add(home_url)

            # Handle description
            description_div = home.find('div', class_='sc-620b3daf-1 lgLxys')

            if description_div:
                description_spans = description_div.find_all('span')
                if description_spans:
                    description = ' | '.join([span.text.strip() for span in description_spans])
                else:
                    description = description_div.text.strip() if description_div.text.strip() else 'N/A'
            else:
                description = 'N/A'

            home_data = {
                'Category': category.text if category else 'N/A',
                'Location': location.text if location else 'N/A',
                'Price': price.text if price else 'N/A',
                'Description': description,
                'Home_Url': home_url,
            }

            page_homes.append(home_data)

        except Exception as e:
            print(f"  Error scraping a home: {e}")
            continue

    if duplicates_found > 0:
        print(f"  ⚠️ Skipped {duplicates_found} duplicate(s) on this page")

    return page_homes


def scrape_all_daft():
    """Scrape ALL properties from Daft.ie Ireland"""
    print("=" * 100)
    print("Daft.ie Property Scraper - ALL IRELAND")
    print("=" * 100 + "\n")

    driver = webdriver.Chrome()
    driver.maximize_window()

    all_homes = []
    seen_urls = set()
    page = 1
    consecutive_empty_pages = 0
    max_empty_pages = 3

    try:
        while True:
            url = build_daft_url(page)
            print(f"Scraping page {page}...")

            page_homes = scrape_daft_page(driver, url, seen_urls)

            if not page_homes:
                consecutive_empty_pages += 1
                print(f"  ⚠️ No new homes found on page {page} (empty count: {consecutive_empty_pages})")

                if consecutive_empty_pages >= max_empty_pages:
                    print(f"\n✓ Reached end after {page} pages")
                    break
            else:
                consecutive_empty_pages = 0
                all_homes.extend(page_homes)
                print(f"  ✓ Found {len(page_homes)} unique homes on page {page}")
                print(f"  Total unique homes so far: {len(all_homes)}\n")

            page += 1
            time.sleep(2)

    finally:
        driver.quit()

    return all_homes


if __name__ == "__main__":
    # Scrape all properties
    all_homes = scrape_all_daft()

    print("\n" + "=" * 100)
    print("SCRAPING COMPLETE")
    print("=" * 100)
    print(f"Total unique homes scraped: {len(all_homes)}")

    if all_homes:
        df = pd.DataFrame(all_homes)

        # Remove any duplicates
        duplicate_count = df['Home_Url'].duplicated().sum()
        if duplicate_count > 0:
            print(f"\n⚠️ Found {duplicate_count} duplicate URLs, removing...")
            df = df.drop_duplicates(subset=['Home_Url'], keep='first')

        # Save with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d')
        filename = f"daft_properties_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"\n✓ Saved {len(df)} properties to {filename}")

        # Display first 10 homes
        print("\nFirst 10 properties:")
        for i, home in enumerate(all_homes[:10], 1):
            print(f"{i}. {home['Category']} - {home['Location']} - {home['Price']}")
    else:
        print("\n⚠️ No homes found")