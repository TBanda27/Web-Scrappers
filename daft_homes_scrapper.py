from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

homes_url = "https://www.daft.ie/property-for-rent/dublin?rentalPrice_from=1000&rentalPrice_to=2000&page=1"

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(homes_url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

homes_html = soup.find('ul', class_='sc-798c155d-4 kmVnWY')
homes_items = homes_html.find_all('li')

print(f"Found {len(homes_items)} homes on page 1\n")

# Store all homes in a list
all_homes = []

for index, home in enumerate(homes_items, 1):
    try:
        price = home.find('p', class_='sc-af41020b-0 dqCzFn')
        category = home.find('p', class_='sc-af41020b-0 btpgrM')
        location = home.find('p', class_='sc-af41020b-0 dVPJAx')
        house_url = home.find('a', class_='sc-798c155d-19 cDtUBM')

        if not category and not location:
            continue

        # Handle description with proper error checking
        description_div = home.find('div', class_='sc-620b3daf-1 lgLxys')

        if description_div:
            # Find ALL spans (not just one)
            description_spans = description_div.find_all('span')

            if description_spans:
                # Extract text from all spans
                description = [span.text.strip() for span in description_spans]
                # Join them into a single string (or keep as list)
                description = ' | '.join(description)  # e.g., "3 beds | 2 baths | House"
            else:
                # Div exists but no spans - get text directly from div
                description = description_div.text.strip() if description_div.text.strip() else 'N/A'
        else:
            # No description div at all
            description = 'N/A'

        home_data = {
            'Category': category.text if category else 'N/A',
            'Location': location.text if location else 'N/A',
            'Price': price.text if price else 'N/A',
            'Description': description,
            'Home_Url' : homes_url if homes_url else 'N/A',
        }

        all_homes.append(home_data)

        # Print as we go
        print(
            f"{index}. {home_data['Category']} - {home_data['Location']} - {home_data['Price']} - {home_data['Description']} - {home_data['Home_Url']}")

    except Exception as e:
        print(f"{index}. Error: {e}")
        continue

# Save to CSV
df = pd.DataFrame(all_homes)
df.to_csv('daft_homes_page1.csv', index=False)
print(f"\n✓ Saved {len(all_homes)} homes to daft_homes_page1.csv")