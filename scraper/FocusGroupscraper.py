import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class FocusGroupsScraper:
    def __init__(self, database, headless, messaging_service, username, password, login_url='https://app.focusgroups.org/my'):
        self.database = database
        self.username = username
        self.password = password
        self.login_url = login_url
        self.headless = headless
        self.messaging_service = messaging_service
        self.driver = None

    def login(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.login_url)
        time.sleep(3)

        # Enter username and password
        self.driver.find_element(By.ID, "email").send_keys(self.username)  # Adjust the ID as necessary
        self.driver.find_element(By.ID, "password").send_keys(self.password)  # Adjust the ID as necessary
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'SUBMIT')]").click()  # Adjust the button text as necessary
        time.sleep(3)

    async def scrape_focus_groups(self):
        if not self.driver:
            self.login()

        # Navigate to the target page
        elements = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > mat-sidenav-container > mat-sidenav-content > div > div > app-groups > div > div.items > app-group-item > div > div.job__item-action > a")
        view_button= elements[0]
        view_button.click()
        time.sleep(2)
        # Locate all paragraphs matching the CSS selector
        paragraphs = self.driver.find_elements(By.CSS_SELECTOR, "#app > div > mat-sidenav-container > mat-sidenav-content > div > div > study-details > div > div.items > div > div.description")

        # Initialize an empty string to hold the description
        description = ""
        # Iterate through the paragraphs and append their text to the description
        for paragraph in paragraphs:
            description += paragraph.text + "\n"  # Add a newline after each paragraph
        # Locate the container div holding all the labels and spans
        container = self.driver.find_element(By.CSS_SELECTOR, "#app > div > mat-sidenav-container > mat-sidenav-content > div > div > study-details > div > div.items > div > div.study-details > div")

        # Find all label and span elements within the container
        labels = container.find_elements(By.CSS_SELECTOR, "label")
        spans = container.find_elements(By.CSS_SELECTOR, "span")

        # Initialize an empty string to store the result
        result = ""

        # Iterate over both lists simultaneously
        for label, span in zip(labels, spans):
            result += f"{label.text} {span.text}\n"
        
        link= self.driver.find_element(By.CSS_SELECTOR, "#app > div > mat-sidenav-container > mat-sidenav-content > div > div > study-details > div > div.items > div > a:nth-child(6)")
        time.sleep(2)
        
        if("L&E Research" not in result and "FieldWork" not in result ):
            answer = f"{description}\n{result}\nLink: {link.get_attribute('href')}"
            if not self.database.is_answer_in_db(answer):
                self.database.save_answer_to_db(answer, link.get_attribute('href'), "FocusGroups")
                await self.messaging_service.send_message(answer)
            else:
                print("Focus Group Study already in database.")
        
        self.driver.quit()
        self.driver = None