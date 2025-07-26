# Web-Scrpaing_Task

Scraping Logic
The script automates browsing the Earth911 search results using Selenium in headless mode. It handles pagination by iterating through multiple pages, dynamically updating the URL with the page number. For each page, it waits explicitly until all facility listings load before extracting data. The scraper collects the business name, concatenated street address (from multiple address fields), and accepted materials for each facility.

Data cleaning is performed by removing invisible Unicode characters and trimming extra whitespace to ensure clean, readable text. Error handling is implemented with try/except blocks around each data extraction step to gracefully handle missing or malformed elements without interrupting the scraping process.

Libraries and Tools Used
Selenium: Chosen for its ability to interact with dynamic, JavaScript-rendered web content, which is common on modern websites like Earth911.

webdriver-manager: Simplifies managing ChromeDriver versions automatically, avoiding manual setup issues.

re (Regular Expressions): Used to clean and sanitize extracted text by removing hidden or special characters.

csv: Python’s built-in module for writing the structured scraped data into a CSV file, allowing easy export and analysis.

Proposed Approach if Script Was Incomplete
If the full script was not completed, my approach would still center around using Selenium due to the site’s dynamic content. I would use explicit waits to ensure elements load before scraping, and paginate either by detecting a “next” button or iterating over a known number of pages.

Potential challenges include dealing with site anti-scraping measures like rate limiting or CAPTCHAs. To address these, I would introduce randomized delays between requests, rotate user-agent strings, and consider proxy usage to distribute traffic. Data cleaning and error handling would be implemented similarly, using regular expressions for text sanitization and try/except blocks for robustness. The final data would be stored in CSV or JSON format for easy use downstream.

