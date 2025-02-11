import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

class BayAreaFocusGroupsScsraper:
    def __init__(self, database, headless, username, messaging_service, password, login_url='https://www.bayareafocusgroups.com/wp-login.php', target_url='https://www.bayareafocusgroups.com/'):
        """
        Initializes the BayAreaFocusGroups class with login credentials, database, and target URLs.
        """
        self.database = database
        self.username = username
        self.password = password
        self.login_url = login_url
        self.headless= headless
        self.target_url = target_url
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
        self.driver.find_element(By.ID, "user_login").send_keys(self.username)
        self.driver.find_element(By.ID, "user_pass").send_keys(self.password)
        self.driver.find_element(By.ID, "wp-submit").click()
        time.sleep(3)

    async def scrape_bay_area(self):
        """
        Logs in if necessary, then scrapes study listings and saves new studies to the database.
        """
        # Ensure login is complete before scraping
        if not self.driver:
            self.login()

        # Navigate to the target page
        self.driver.get(self.target_url)
        time.sleep(3)

        # Access the first post link
        elements = self.driver.find_elements(By.CSS_SELECTOR, "h3.gridview-grid-post-title a")
        if elements:
            elements[0].click()
            time.sleep(3)

            # Get the title and list elements
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.post-title.entry-title").text
            ul_element = self.driver.find_element(By.CLASS_NAME, "wp-block-list")
            li_elements = ul_element.find_elements(By.TAG_NAME, "li")
            
            # Concatenate text from all <li> elements except the last
            result = "\n".join([li.text for li in li_elements[:-1]])

            # Get the href attribute from the link element
            a_element = self.driver.find_element(By.LINK_TEXT, "Open screener in a new tab")
            href_value = a_element.get_attribute("href")

            # Format the answer
            answer = f"{title}\n{result}\nLink: {href_value}"
            
            if "L&E Opinions" not in answer and not self.database.is_answer_in_db(answer):
                self.database.save_answer_to_db(answer, href_value, "Bay Area Focus Groups")
                await self.messaging_service.send_message(answer)
            else:
                print("Bay Area Focus Group already in database.")

        time.sleep(3)
        # Close the driver session
        self.driver.quit()
        self.driver = None
        
    async def handle_message(self, answer):
            await self.messaging_service.send_message(answer)