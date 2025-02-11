
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class FieldworkScraper:
    def __init__(self, database, headless, messaging_service, email, password, login_url='https://participate.fieldwork.com/Account/Login?ReturnUrl=%2F', target_url='https://www.fieldwork.com/studies'):
        """
        Initializes the FieldworkScraper class with login credentials, database, and target URLs.
        """
        self.database = database
        self.email = email
        self.password = password
        self.login_url = login_url
        self.headless = headless
        self.target_url = target_url
        self.messaging_service = messaging_service
        self.driver = None


    def login(self):
        """
        Logs in to Fieldwork using provided email and password.
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.login_url)
        time.sleep(3)
        
        # Enter email and password
        self.driver.find_element(By.ID, "close").click()
        self.driver.find_element(By.ID, "Email").send_keys(self.email)
        self.driver.find_element(By.ID, "Password").send_keys(self.password)
        self.driver.find_element(By.ID, "login-submit-btn").click()  
        time.sleep(3)

    async def scrape_fieldwork_studies(self):
        """
        Logs in if necessary, then scrapes study listings and saves new studies to the database.
        """
        # Ensure login is complete before scraping
        if not self.driver:
            self.login()
        time.sleep(3)
        
        titles= self.driver.find_elements(By.ID, "survey-name-preview")
        descriptions= self.driver.find_elements(By.ID, "survey-body-preview")
        
        
        for title, description in list(zip(titles, descriptions))[:12]:
            finalString=""
            answer=""
            finalString= title.text + "\n" + description.text + "\n"
            answer= finalString + title.get_attribute('href') + "\n"
            if not self.database.is_answer_in_db(finalString):
                self.database.save_answer_to_db(finalString, title.get_attribute('href'), "Fieldwork")
                await self.messaging_service.send_message_shiga(answer)
        time.sleep(3)
        # Close the driver session
        self.driver.quit()
        self.driver = None