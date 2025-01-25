import time
import asyncio
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class UserInterviewsScraper:
    def __init__(self, database, headless, messaging_service, cookies, url='https://www.userinterviews.com/studies/referrals?sort=-id'):
        """
        Initializes the UserInterviews class with database, cookies, and the target URL.
        """
        self.database = database
        self.cookies = cookies
        self.url = url
        self.driver = None
        self.headless = headless
        self.messaging_service = messaging_service

    def scrape_user_interviews(self):
        """
        Logs in using cookies, scrapes study listings, and saves new studies to the database.
        """
        # Setup Chrome driver
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        time.sleep(3)

        # Adding cookies to the browser session for login
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(self.url)  # Reload the page after setting cookies
        time.sleep(5)

        # Try to close any potential sign-in pop-up or warning
        try:
            print("Trying to close any sign-in or pop-up buttons...")
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='close warning']").click()
        except NoSuchElementException:
            print("No pop-up found, continuing...")

        # Find study elements on the page
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".Card.ProjectListing")

        for i, element in enumerate(elements[:3]):  # Limiting to first 3 elements
            # Extract relevant data from each study listing
            title = element.find_element(By.CSS_SELECTOR, "h2.ProjectListing__title").text
            price = element.find_element(By.CSS_SELECTOR, "div.ProjectListing__compensation").text
            clipboard_button = element.find_element(By.CSS_SELECTOR, ".CopyToClipboardButton.btn")
            ActionChains(self.driver).scroll_to_element(clipboard_button).perform()
            clipboard_button.click()
            link = pyperclip.paste()  # Copy the link to clipboard

            items = element.find_elements(By.CSS_SELECTOR, "li.ListingCategoryIcons__item")
            study_type = items[0].find_element(By.CSS_SELECTOR, "span.ListingCategoryIcons__name").text
            online_element = items[1].find_element(By.CSS_SELECTOR, "span.ListingCategoryIcons__name").text
            description = element.find_element(By.CSS_SELECTOR, "p.ProjectListing__description").text
            requirements = element.find_element(By.CSS_SELECTOR, "div.ProjectListing__detail").text
            dates = element.find_element(By.CSS_SELECTOR, ".ProjectListing__detail-study-dates-string").text

            # Format the full and simplified answers
            answer = (
                f"{title} ({price})\n\n"
                f"{link}\n\n"
                f"{study_type}\n"
                f"{online_element}\n\n"
                f"{description}\n\n"
                f"{requirements}\n\n"
                f"Dates: {dates}\n"
            )
            fake_answer = (
                f"{title} ({price})\n\n"
                f"{study_type}\n"
                f"{online_element}\n\n"
                f"{description}\n\n"
                f"{requirements}\n\n"
                f"Dates: {dates}\n"
            )

            # Check if the answer is already in the database
            if self.database.is_answer_in_db(fake_answer):
                print("Study already exists in the database.")
            else:
                self.database.save_answer_to_db(fake_answer)
                asyncio.run(self.handle_message(answer))
                time.sleep(5)

        # Close the browser session
        self.driver.quit()
    async def handle_message(self, answer):
            await self.messaging_service.send_message(answer)
