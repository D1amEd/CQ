import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

class GromotionScraper:
    def __init__(self, database, headless, messaging_service, url='https://www.gromotion.co.uk/current-projects'):
        """
        Initializes the BayAreaFocusGroups class with login credentials, database, and target URLs.
        """
        self.database = database
        self.url = url
        self.headless= headless
        self.messaging_service = messaging_service
        self.driver = None

    def login(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        time.sleep(3)

    async def scrape_gromotion(self):
        """
        Logs in if necessary, then scrapes study listings and saves new studies to the database.
        """
        # Ensure login is complete before scraping
        if not self.driver:
            self.login()

        # Locate the element by its href attribute
        element = self.driver.find_element(By.CSS_SELECTOR, "a.basic-button.w-button")

        # Example: click the element
        element.click()
        
        container =self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div")
        text= container.text
        markers = ["LIKE TO GET INVOLVED?", "‍NEXT STEPS:"]

        # Find all indices where a marker is found
        marker_indices = [text.find(marker) for marker in markers if text.find(marker) != -1]

        # If at least one marker is found, get the earliest occurrence
        if marker_indices:
            first_marker_index = min(marker_indices)
            text= text[:first_marker_index].rstrip()
       
        link= self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[1]/div/div/div[2]/div/a")
        link= link.get_attribute("href")
        answer = f"{text}\n{link}"
        
        if not self.database.is_answer_in_db(text):
                self.database.save_answer_to_db(text, link, "Gromotion")
                await self.messaging_service.send_message(answer)
        else:
            print("Gromotion Study already in database.")
        
        time.sleep(3)
        # Close the driver session
        self.driver.quit()
        self.driver = None
        
    async def handle_message(self, answer):
            await self.messaging_service.send_message(answer)