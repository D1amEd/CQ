from database.database import Database
from scraper.bayAreaScraper import BayAreaFocusGroupsScsraper
from scraper.facebookScraper import FacebookScraper
from scraper.lyeScraper import LyEScraper
from scraper.userInterviewsScraper import UserInterviewsScraper
from scraper.FocusGroupscraper import FocusGroupsScraper
from scraper.FieldWorkScraper import FieldworkScraper
from services.message_service import MessagingService
from scraper.gromotionScraper import GromotionScraper
from scraper.respondentScraper import RespondentScraper
from scraper.prcmarketScraper import PrcMarketScraper
from dotenv import load_dotenv
import asyncio
import os
import json
import threading
from termcolor import colored

print(colored("Starting main.py", "green"))


def load_cookies(file_path):
    with open(file_path, 'r') as file:
        cookies = json.load(file)
    return cookies

user_interview_cookies = load_cookies('user_interview_cookies.json')
respondent_cookies = load_cookies('respondent_cookies.json')

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
lyeScrapper= LyEScraper(database=database, headless= True, messaging_service=messagingServce, email=os.getenv("LYE_USER"), password=os.getenv("LYE_PASSWORD"))
userInterviewsScrapper= UserInterviewsScraper(database=database, headless=True, messaging_service=messagingServce, cookies=user_interview_cookies)
focusGroupsScraper = FocusGroupsScraper(database=database, headless=True, username=os.getenv("FOCUS_GROUP_USERNAME"), password=os.getenv("FOCUS_GROUP_PASSWORD"), messaging_service=messagingServce)
fieldworkScraper = FieldworkScraper(database=database, headless=True, email=os.getenv("FIELD_WORK_USERNAME"), password=os.getenv("FIELD_WORK_PASSWORD"), messaging_service=messagingServce)
gromotionScraper = GromotionScraper(database=database, headless=True, messaging_service=messagingServce)
respondentScraper = RespondentScraper(database=database, messaging_service=messagingServce)
prcScraper= PrcMarketScraper(database=database, headless=True, messaging_service=messagingServce)
INTERVAL_SECONDS = 600
async def lye_task():
    """Run LyeScraper indefinitely every X seconds."""
    while True:
        try:
            print("[LyeScraper] Starting scrape")
            await lyeScrapper.scrape_lye_studies()
            print("[LyeScraper] Finished scrape")
        except Exception as e:
            print(colored(f"Error in LyeScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in LyeScraper: {e}")
        await asyncio.sleep(INTERVAL_SECONDS)
        
async def focus_groups_task():
    """Run FocusGroupsScraper indefinitely every X seconds."""
    while True:
        try:
            print("[FocusGroups] Starting scrape")
            await focusGroupsScraper.scrape_focus_groups()
            print("[FocusGroups] Finished scrape")
        except Exception as e:
            print(colored(f"Error in FocusGroupsScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in FocusGroupsScraper: {e}")
        await asyncio.sleep(INTERVAL_SECONDS)

async def bayarea_task():
    """Run BayAreaFocusGroupsScrsraper indefinitely every X seconds."""
    while True:
        try:
            print("[BayArea] Starting scrape")
            await bayareaScrapper.scrape_bay_area()
            print("[BayArea] Finished scrape")
        except Exception as e:
            print(colored(f"Error in BayAreaFocusGroupsScsraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in BayAreaFocusGroupsScsraper: {e}")
        await asyncio.sleep(INTERVAL_SECONDS)
        
async def user_interviews_task():
    """Run UserInterviewsScraper indefinitely every X seconds."""
    await asyncio.sleep(10)
    while True:
        try:
            print("[UserInterviews] Starting scrape")
            await userInterviewsScrapper.scrape_user_interviews()
            print("[UserInterviews] Finished scrape")
        except Exception as e:
            print(colored(f"Error in UserInterviewsScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in UserInterviewsScraper: {e}")

        await asyncio.sleep(INTERVAL_SECONDS)
    
async def gromotion_task():
    """Run GromotionScraper indefinitely every X seconds."""
    await asyncio.sleep(10)
    while True:
        try:
            print("[Gromotion] Starting scrape")
            await gromotionScraper.scrape_gromotion()
            print("[Gromotion] Finished scrape")
        except Exception as e:
            print(colored(f"Error in GromotionScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in GromotionScraper: {e}")
        await asyncio.sleep(INTERVAL_SECONDS)
        
async def fieldwork_task():
    """Run FieldworkScraper indefinitely every X seconds."""
    await asyncio.sleep(60)
    while True:
        try:
            print("[Fieldwork] Starting scrape")
            await fieldworkScraper.scrape_fieldwork_studies()
            print("[Fieldwork] Finished scrape")
        except Exception as e:
            print(colored(f"Error in FieldworkScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in FieldworkScraper: {e}")
        await asyncio.sleep(INTERVAL_SECONDS)

async def respondent_task():
    """Run RespondentScraper indefinitely every X seconds."""
    while True:
        try:
            print("[Respondent] Starting scrape")
            await respondentScraper.print_projects()
            print("[Respondent] Finished scrape")
        except Exception as e:
            print(colored(f"Error in RespondentScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in RespondentScraper: {e}")
        await asyncio.sleep(INTERVAL_SECONDS)
        
async def prc_task():
    """Run PRC indefinitely every X seconds."""
    while True:
        try:
            print("[PRC] Starting scrape")
            await prcScraper.scrape_prc_studies()
            print("[PRC] Finished scrape")
        except Exception as e:
            print(colored(f"Error in PRCScraper: {e}", "red"))
            messagingServce.send_message_email_eddie(f"Error in PRCScraper: {e}")
        await asyncio.sleep(1500)

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
run_task_in_thread(bayarea_task, "BayArea Task")
run_task_in_thread(user_interviews_task, "User Interviews Task")
run_task_in_thread(focus_groups_task, "Focus Groups Task")
run_task_in_thread(fieldwork_task, "Field Work Task")
run_task_in_thread(gromotion_task, "Gromotion Task")
run_task_in_thread(respondent_task, "Responder Task")
run_task_in_thread(prc_task, "PRC Task")

# Keep the main thread alive (e.g., waiting for user input or other tasks)
try:
    while True:
        pass  # Simulate the main thread doing other work
except KeyboardInterrupt:
    print('Main thread exiting.')
        

# # Entry point
# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print('Exiting...')
