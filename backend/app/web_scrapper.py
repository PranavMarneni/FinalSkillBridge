import requests
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
import time


logging.basicConfig(level=logging.INFO)

def validate_job_url(url):
    valid_domains = [
        'ziprecruiter.com', 'craigslist.org', 'simplyhired.com',
        'reed.co.uk', 'dice.com', 'facebook.com/jobs', 'indeed.com',
        'greenhouse.io', 'lever.co', 'workday.com', 'smartrecruiters.com',
        'myworkdayjobs.com', 'jobs.lever.co', 'boards.greenhouse.io'
    ]
    return any(domain in url for domain in valid_domains)

def get_selenium_page(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        logging.info(f"Navigating to URL: {url}")
        driver.get(url)
        
        time.sleep(5)  # Wait for page to load
        
        page_source = driver.page_source
        driver.quit()
        return page_source
    except Exception as e:
        logging.error(f"Error fetching page with Selenium: {e}")
        return None

def extract_job_details(soup, url):
    # Build a long string containing the job details
    job_details_str = f"Job URL: {url}\n"
    
    if 'indeed.com' in url:
        
        title = soup.select_one('h1.jobsearch-JobInfoHeader-title')
        if title:
            job_details_str += f"Title: {title.text.strip()}\n"
        else:
            #logging.warning("Could not find job title")
            job_details_str += "Title: Not found\n"
        
        company = soup.select_one('div[data-company-name="true"]')
        if company:
            job_details_str += f"Company: {company.text.strip()}\n"
        else:
            #logging.warning("Could not find company name")
            job_details_str += "Company: Not found\n"
        
        location = soup.select_one('div[data-testid="job-location"]')
        if location:
            job_details_str += f"Location: {location.text.strip()}\n"
        else:
            #logging.warning("Could not find job location")
            job_details_str += "Location: Not found\n"
        
        description = soup.select_one('div#jobDescriptionText')
        if description:
            job_details_str += f"Description: {description.text.strip()}\n"
        else:
            #logging.warning("Could not find job description")
            job_details_str += "Description: Not found\n"
    
    return job_details_str

# In web_scrapper.py
def get_job_details(url):
    # Import royce inside the function to avoid circular import issues
    from .royce import getSkillSet  # Move the import here

    # Rest of your function logic...
    page_source = get_selenium_page(url)
    if page_source:
        soup = BeautifulSoup(page_source, 'html.parser')
        return extract_job_details(soup, url)
    return None


def main_method(urls):
    jobScrapeList = []
    
    for url in urls:  # Use 'urls' parameter instead of 'jobUrlList'
        if validate_job_url(url.url):  # Adjust based on how URLs are stored in the model
            job_data = get_job_details(url.url)
            if job_data:
                jobScrapeList.append(job_data)  # Collect job data
    
    if jobScrapeList:
        # Extract the required skills from the scraped jobs
        extracted_skills = getSkillSet(jobScrapeList)

        # Assuming you have the PDF resume already loaded, generate the study plan
        pdf_path = "/Users/pranavmarneni/Downloads/Main_Resume-2.pdf"
        pdf_text = pdf_to_string(pdf_path)

        if pdf_text:
            # Generate a study plan based on the resume text and extracted skills
            study_plan = createStudyPlan(pdf_text, extracted_skills)
            
            return study_plan  # Return the generated study plan
        else:
            logging.error("Failed to extract text from PDF.")
            return []
    else:
        return []


if __name__ == "__main__":
    scraped_jobs_list = main()
    if scraped_jobs_list:
        print("\nFinal Scraped Jobs List (Strings):")
        for job_str in scraped_jobs_list:
            print(job_str)  # Print each long string
            print("-" * 80)  # Separator for readability
