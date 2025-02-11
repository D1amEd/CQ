import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

class PrcMarketScraper:
    def __init__(self, database, headless, messaging_service, url='https://www.prcmarketresearch.com/upcomingprojects'):
        """
        Initializes the BayAreaFocusGroups class with login credentials, database, and target URLs.
        """
        self.database = database
        self.url = url
        self.headless= headless
        self.messaging_service = messaging_service
        self.driver = None

    async def scrape_prc_studies(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        time.sleep(3)
        try:
            # Locate the element by its href attribute
            close_button = self.driver.find_element(By.ID, "comp-llqyc2i8")
            close_button.click()
        except NoSuchElementException:
            print("No element found.")
        # Locate the element by its href attribute
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'p.font_9.wixui-rich-text__text')
        link= self.driver.find_element(By.CSS_SELECTOR, "a.wixui-rich-text__text")
        text= ""
        for i, element in enumerate(elements[:3]):
            if("~~~~~~~~~~~~~~~" in element.text):
                break
            text+= element.text + "\n"
        # Split the text into lines
        lines = text.split("\n")

        # Check if the first line contains "Added" and remove it
        if lines[0].lower().startswith("added"):
            lines.pop(0)  # Remove the first line

        # Join the lines back into a single string
        text = "\n".join(lines)
        if self.database.is_answer_in_db(text):
            print("PRC Market Study already in database.")
        else:
            self.database.save_answer_to_db(text, link.get_attribute('href'), "PRC Market")
            text+= f"Referral Link: {link.get_attribute('href')}\n"
            await self.handle_message(text)
            await asyncio.sleep(2)
            
        
        time.sleep(3)
        # Close the driver session
        self.driver.quit()
        
    async def handle_message(self, answer):
            await self.messaging_service.send_message(answer)