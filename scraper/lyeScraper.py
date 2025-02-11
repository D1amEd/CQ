import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class LyEScraper:
    def __init__(self, database, headless, messaging_service, email, password, login_url='https://participant.facilitymanagerplus.com/Participant/AvailableStudies.aspx'):
        """
        Initializes the LyEScraper class with login credentials, database, and the target URL.
        """
        self.database = database
        self.email = email
        self.password = password
        self.login_url = login_url
        self.headless = headless
        self.messaging_service = messaging_service
        self.driver = None

    def _setup_driver(self):
        """
        Set up the Chrome driver with options.
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        """
        Logs in to L&E Research using provided email and password.
        """
        self._setup_driver()
        self.driver.get(self.login_url)
        time.sleep(3)

        # Enter email and password
        self.driver.find_element(By.ID, "ctl00_cphBody_EmailTextBox").send_keys(self.email)
        self.driver.find_element(By.ID, "ctl00_cphBody_PasswordTextBox").send_keys(self.password)
        
        # Click on the captcha checkbox (or other login button if applicable)
        captcha_button = self.driver.find_element(By.CLASS_NAME, "g-recaptcha")
        captcha_button.click()
        time.sleep(3)

    async def scrape_lye_studies(self):
        """
        Logs in if necessary, then scrapes study listings and saves new studies to the database.
        """
        # Ensure login is complete before scraping
        if not self.driver:
            self.login()

        # Find and process the study elements
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div.project-detail")

        for i, element in enumerate(elements[:3]):  # Limiting to first 3 elements
            # Extract relevant data from each study listing
            title = element.find_element(By.CSS_SELECTOR, "h3").text
            compensation=""
            
            try:
                compensation = element.find_element(By.XPATH, ".//li[i[contains(@class, 'fa-dollar-sign')]]").text
            except NoSuchElementException:
                compensation = "No compensation listed"
            location = element.find_element(By.CLASS_NAME, "fa-location-dot").find_element(By.XPATH, "..").text
            age = element.find_element(By.CLASS_NAME, "fa-cake-candles").find_element(By.XPATH, "..").text
            gender = element.find_element(By.CLASS_NAME, "fa-user").find_element(By.XPATH, "..").text
            study_type=""
            try:
                study_type = element.find_element(By.CLASS_NAME, "fa-comment").find_element(By.XPATH, "..").text
            except NoSuchElementException:
                study_type = "No Study listed"
            photo_id = element.find_element(By.CLASS_NAME, "fa-id-card").find_element(By.XPATH, "..").text
            description = element.find_element(By.CSS_SELECTOR, "p").text
            link = element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            # Format the answer
            answer = (
                f"{title}\n{compensation}\n{location}\n{age}\n{gender}\n{study_type}\n{photo_id}\n"
                f"{description}\nLink: {link}"
            )

            await self.handle_message(answer, link)
            time.sleep(5)

        # Close the driver session
        self.driver.quit()
        self.driver = None
        
    async def handle_message(self, answer, link):
        if self.database.is_answer_in_db(answer):
            print("Lye study answer already in database.")
        else:
            self.database.save_answer_to_db(answer, link, "L&E Research")
            await self.messaging_service.send_message(answer)  # Await the async method
            await asyncio.sleep(5)  # Replace `time.sleep` with `await asyncio.sleep`
    

