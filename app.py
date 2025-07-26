import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def clean_text(text):
    if not text:
        return text
    cleaned = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
    return cleaned.strip()

def scrape_earth911():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = "https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=100&page={}"
    results = []

    for page in range(1, 3):
        url = base_url.format(page)
        driver.get(url)
        print(f"Scraping page {page}...")

        try:
            facilities = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "result-item"))
            )
        except:
            print(f"No facilities found on page {page}.")
            continue

        for facility in facilities:
            try:
                business_name = clean_text(facility.find_element(By.CSS_SELECTOR, "h2.title a").text)
            except:
                business_name = None

            try:
                contact_div = facility.find_element(By.CLASS_NAME, "contact")
                address1 = clean_text(contact_div.find_element(By.CLASS_NAME, "address1").text)
                address2 = clean_text(contact_div.find_element(By.CLASS_NAME, "address2").text)
                address3 = clean_text(contact_div.find_element(By.CLASS_NAME, "address3").text)
                street_address = ", ".join(filter(None, [address1, address2, address3]))
            except:
                street_address = None

            try:
                materials_parent = facility.find_element(By.CLASS_NAME, "result-materials")
                material_spans = materials_parent.find_elements(By.CSS_SELECTOR, "span.material")
                materials_list = [
                    clean_text(span.text) for span in material_spans
                    if span.text.strip() and not span.text.startswith("+")
                ]
                materials_accepted = ", ".join(materials_list)
            except:
                materials_accepted = None

            results.append({
                "business_name": business_name,
                "street_address": street_address,
                "materials_accepted": materials_accepted
            })

    driver.quit()

    csv_file = "recycling_centers_10001.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["business_name","street_address", "materials_accepted"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Scraping complete. Data saved to '{csv_file}'.")

if __name__ == "__main__":
    scrape_earth911()
