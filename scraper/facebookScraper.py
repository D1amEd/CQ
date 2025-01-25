import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

class FacebookScraper:
    def __init__(self, database, headless, messaging_service, cookies, url='https://www.facebook.com/groups/2352078735120624'):
        """
        Initializes the FacebookScraper with database and scraping configurations.
        """
        self.database = database
        self.cookies = cookies
        self.headless = headless
        self.url = url

    def facebook_scraper(self):
        """
        Scrapes posts from a Facebook group and saves new ones to the database.
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        action = ActionChains(driver)
        
        driver.get(self.url)
        time.sleep(2)
        
        # Add cookies to the session
        for cookie in self.cookies:
            driver.add_cookie(cookie)
        time.sleep(2)
        
        driver.get(self.url)

        try:
            # Click on a specific element to load more posts if required
            element = driver.find_element(By.CSS_SELECTOR, 'div.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xzsf02u.x1s688f')
            element.click()
        except NoSuchElementException:
            print("Element not found, skipping...")

        elements = driver.find_elements(By.CSS_SELECTOR, 'span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u')

        for element in elements:
            href_elements = element.find_elements(By.TAG_NAME, 'a')
            if len(element.text) > 30:
                if "https" in element.text:
                    start_index = element.text.find("https")
                    end_index = element.text.find(" ", start_index)
                    if end_index == -1:
                        end_index = len(element.text)
                    url_beginning = element.text[start_index:start_index + 17]
                    url_text = element.text[start_index:end_index]
                    answer = element.text
                    fake_answer = answer.replace(url_text, "")

                    for href_element in href_elements:
                        try:
                            action.move_to_element(href_element).perform()
                            href = href_element.get_attribute('href')
                        except:
                            continue
                        if href and url_beginning in href:
                            new_text = element.text.replace(url_text, href)
                            answer = new_text
                            break

                    if self.database.is_answer_in_db(fake_answer):
                        print("Answer already exists in the database.")
                    else:
                        self.database.save_answer_to_db(fake_answer)
                        print("New answer saved to the database:", answer)
                        self.messaging_service.send_message(answer)
                        print("----")

        time.sleep(5)
        driver.quit()

