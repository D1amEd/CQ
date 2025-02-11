import asyncio
import requests


class RespondentScraper:
    def __init__(self, database, messaging_service):
        # API endpoint
        self.url = "https://app.respondent.io/api/v4/matching/projects/search/profiles/5ff568ddcac8780029ef3ac1"
        self.database=  database
        self.messaging_service = messaging_service
        # Query parameters to be sent with the GET request
        self.params = {
            "maxIncentive": "1000",
            "minIncentive": "5",
            "maxTimeMinutesRequired": "800",
            "minTimeMinutesRequired": "5",
            "talkToAudience": "2",
            "sort": "publishedAt",
            "pageSize": "15",
            "page": "1",
            "includeCount": "false",
            "gender": "male",
            "educationLevel": "highschoolgraduate",
            "ethnicity": "hispaniclatino",
            "dateOfBirth": "1994-05-27",
            "showHiddenProjects": "true",
            "onlyShowMatched": "false",
            "showEligible": "true",
            "country": "US"
        }
        
        # Headers required by the API
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,es;q=0.7",
            "Authorization": ("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                              "eyJpZCI6IjVmZjU2OGRkODYyNThlMDAxMTYyMGU2ZiIsImZpcnN0TmFtZSI6"
                              "IlNlcmdpbyIsImxhc3ROYW1lIjoiQ29ycmVhIE1hcnRpbmVuZ28iLCJlbWFp"
                              "bCI6InNlcmdpb21hcnRpbmVuZ29AaG90bWFpbC5jb20iLCJpYXQiOjE3Mzg3"
                              "MDMxMDQsImV4cCI6MTczODc0NjMwNH0.M54o7K6ObRVGjLZs378k2AKhEQB60z0nzUsZcXHG878"),
            "Cookie": ("_csrf=xWFut6N47cr0_M_CHEFV4DHl; intercom-id-mzi9ntpw=d919f57f-fdf9-4bf5-adb0-fc61c21429ad; intercom-session-mzi9ntpw=; intercom-device-id-mzi9ntpw=2e0d49a6-d1c4-4f0b-ac44-fc2db7005526; consentMode=%7B%22security_storage%22%3A%22granted%22%2C%22analytics_storage%22%3A%22granted%22%2C%22functionality_storage%22%3A%22granted%22%2C%22personalization_storage%22%3A%22granted%22%2C%22ad_storage%22%3A%22granted%22%7D; respondent.referralCode=320df555-0f57-4ca2-8c74-890729c26ddf; XSRF-TOKEN=nQdHUzHK-oShhK7QSHk6QQs1PQDU-GZiPMt4; respondent.session.sid=s%3Aac63sVQOW1e3RdPQyjQ9XMO_N1Snh0qL.Iw7dINLCnpg9jcEatPb0AE0%2Fw1qVVKH%2Bn5VqUIjlWpc"),
            "Sec-Ch-Ua": "'Not A;Brand';v='8', 'Chromium';v='132', 'Google Chrome';v='132'",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/132.0.0.0 Safari/537.36"),
            "X-Requested-With": "XMLHttpRequest",
            "X-Xsrf-Token": "n2RDxVzL_T2NOFVHbp668rOSZA_SRls1t0"
        }
    
    def fetch_projects(self):
        """
        Send a GET request to the Respondent API and return the JSON data.
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching projects: {e}")
            return {}
    
    async def print_projects(self):
        """
        Fetch projects and print out selected information for each project.
        """
        data = self.fetch_projects()
        results = data.get('results', [])
        
        if not results:
            print("No projects found.")
            return
        
        for result in results:
            name = result.get('name')
            description = result.get('description')
            # Get a list of topic names, if available
            topics = [topic.get('name') for topic in result.get('topics', [])]
            remuneration = result.get('respondentRemuneration')
            time_required = result.get('timeMinutesRequired')
            referral_link = result.get('referralLink')
            
            
            text = (
            f"Name: {name}\n"
            f"Description: {description}\n"
            f"Topics: {topics}\n"
            f"Remuneration: {remuneration} $ \n"
            f"Time Required (minutes): {time_required}\n"
            )
            if self.database.is_answer_in_db(text):
                print("Respondent Study already in database.")
                
            else:
                self.database.save_answer_to_db(text, referral_link, "Respondent")
                text += f"Referral Link: {referral_link}\n"
                await self.messaging_service.send_message(text)
                await asyncio.sleep(2)
                
                


