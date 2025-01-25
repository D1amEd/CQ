from database.database import Database
from scraper.bayAreaScraper import BayAreaFocusGroupsScsraper
from scraper.facebookScraper import FacebookScraper
from scraper.lyeScraper import LyEScraper
from scraper.userInterviewsScraper import UserInterviewsScraper
from services.message_service import MessagingService
from dotenv import load_dotenv
import asyncio
import os
import json
import threading



def load_cookies(file_path):
    with open(file_path, 'r') as file:
        cookies = json.load(file)
    return cookies

cookies_file='user_interview_cookies.json'
user_interview_cookies = load_cookies(cookies_file)
# Load environment variables
load_dotenv()

#Get the facebook Cookies
cookies = [
    {'name': 'sb', 'value': os.getenv('COOKIE_sb')},
    {'name': 'datr', 'value': os.getenv('COOKIE_datr')},
    {'name': 'ps_l', 'value': os.getenv('COOKIE_ps_l')},
    {'name': 'ps_n', 'value': os.getenv('COOKIE_ps_n')},
    {'name': 'c_user', 'value': os.getenv('COOKIE_c_user')},
    {'name': 'ar_debug', 'value': os.getenv('COOKIE_ar_debug')},
    {'name': 'dpr', 'value': os.getenv('COOKIE_dpr')},
    {'name': 'presence', 'value': os.getenv('COOKIE_presence')},
    {'name': 'fr', 'value': os.getenv('COOKIE_fr')},
    {'name': 'xs', 'value': os.getenv('COOKIE_xs')},
    {'name': 'wd', 'value': os.getenv('COOKIE_wd')},
]


database= Database()
database.init_db()
messagingServce= MessagingService()
bayareaScrapper= BayAreaFocusGroupsScsraper(database=database, headless=True, username=os.getenv("BAY_AREA_USER"), messaging_service=messagingServce, password=os.getenv("BAY_AREA_PASSWORD"))
facebookScraper= FacebookScraper(database=database, headless=True, messaging_service=messagingServce, cookies=cookies )
lyeScrapper= LyEScraper(database=database, headless=True, messaging_service=messagingServce, email=os.getenv("LYE_USER"), password=os.getenv("LYE_PASSWORD"))
userInterviewsScrapper= UserInterviewsScraper(database=database, headless=True, messaging_service=messagingServce, cookies=user_interview_cookies)


# lyeScrapper.scrape_lye_studies()

async def lye_task():
    print('Running Lye')
    while True:
        await asyncio.to_thread(lyeScrapper.scrape_lye_studies)
        await asyncio.sleep(600)

async def bayArea_task():
    print('Running BayArea')
    while True:
        await asyncio.to_thread(bayareaScrapper.scrape_bay_area)
        await asyncio.sleep(600)
        
async def userInterviews_task():
    print('Running User Interviews')
    while True:
        await asyncio.to_thread(userInterviewsScrapper.scrape_user_interviews)
        await asyncio.sleep(600)
        
# Function to run a task in a thread
def run_task_in_thread(task_func, thread_name):
    def thread_runner():
        print(f"Starting thread: {thread_name}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(task_func())
        except Exception as e:
            print(f"Error in {thread_name}: {e}")
    thread = threading.Thread(target=thread_runner, name=thread_name, daemon=True)
    thread.start()
    
    
    
run_task_in_thread(lye_task, "Lye Task")
run_task_in_thread(bayArea_task, "BayArea Task")
run_task_in_thread(userInterviews_task, "User Interviews Task")

# Keep the main thread alive (e.g., waiting for user input or other tasks)
try:
    while True:
        pass  # Simulate the main thread doing other work
except KeyboardInterrupt:
    print('Main thread exiting.')
        
        
