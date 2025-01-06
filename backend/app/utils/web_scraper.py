import logging
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# ✅ Logging Setup
logging.basicConfig(level=logging.INFO)

# ✅ Valid Domains for Job URLs
VALID_DOMAINS = [
    'ziprecruiter.com', 'craigslist.org', 'simplyhired.com',
    'reed.co.uk', 'dice.com', 'facebook.com/jobs', 'indeed.com',
    'greenhouse.io', 'lever.co', 'workday.com', 'smartrecruiters.com',
    'myworkdayjobs.com', 'jobs.lever.co', 'boards.greenhouse.io'
]

# ✅ 1. Validate Job URL
def validate_job_url(url):
    """Check if the URL belongs to a known job domain."""
    return any(domain in url for domain in VALID_DOMAINS)


# ✅ 2. Initialize Selenium WebDriver
def get_selenium_page(url):
    """Fetch page source from the given URL using Selenium."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logging.info(f"Opening URL: {url}")
        
        driver.get(url)
        time.sleep(5)  # Wait to ensure the page fully loads
        
        page_source = driver.page_source
        driver.quit()
        return page_source
    
    except TimeoutException:
        logging.error("TimeoutException: Page took too long to load.")
        if 'driver' in locals():
            driver.quit()
        return None
    
    except WebDriverException as e:
        logging.error(f"WebDriverException: {e}")
        if 'driver' in locals():
            driver.quit()
        return None


# ✅ 3. Extract Job Details Based on URL
def extract_job_details(soup, url):
    """Parse job details from the page source."""
    details = {"url": url, "description": "Not found", "title": "Unknown", "company": "Unknown"}
    
    try:
        if 'indeed.com' in url:
            title = soup.select_one('h1.jobsearch-JobInfoHeader-title')
            description = soup.select_one('div#jobDescriptionText')
            company = soup.select_one('div.icl-u-lg-mr--sm.icl-u-xs-mr--xs')

            if title:
                details["title"] = title.text.strip()
            if description:
                details["description"] = description.text.strip()
            if company:
                details["company"] = company.text.strip()
        
        elif 'linkedin.com' in url:
            title = soup.select_one('h1.top-card-layout__title')
            description = soup.select_one('div.description')
            company = soup.select_one('a.topcard__org-name-link')

            if title:
                details["title"] = title.text.strip()
            if description:
                details["description"] = description.text.strip()
            if company:
                details["company"] = company.text.strip()
        
        # Add more site-specific scraping logic as needed

    except NoSuchElementException as e:
        logging.warning(f"NoSuchElementException: {e}")
    
    return details


# ✅ 4. Main Function to Get Job Details
def get_job_details(url):
    """Main function to fetch job details from a URL."""
    if not validate_job_url(url):
        logging.warning(f"Invalid URL: {url}")
        return None
    
    page_source = get_selenium_page(url)
    if page_source:
        soup = BeautifulSoup(page_source, 'html.parser')
        return extract_job_details(soup, url)
    
    return None


# ✅ 5. Test Script (Optional)
if __name__ == "__main__":
    test_url = "https://www.indeed.com/jobs?q=software+engineer&l=cumming%2C+ga"
    job_details = get_job_details(test_url)
    print(job_details)
