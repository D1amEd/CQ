from services.smtp_service import GmailSMTPService
from dotenv import load_dotenv
from database.database import Database


import os

load_dotenv()
database= Database()
database.init_db()
print("Database initialized")
#test features

print(database.count_studies_since_yesterday())
# print(database.get_studies_since_yesterday())
print(database.get_study_group_counts())

# gmail_address= os.getenv("GMAIL_ADDRESS")
# gmail_password= os.getenv("GMAIL_PASSWORD")

# smtp_service = GmailSMTPService(gmail_address, gmail_password)
# # Sending an email
# recipient = 'esteban.rico266@gmail.com'
# email_subject = 'Newsletter'
# email_body = 'Hello, this is a test email sent using Gmail SMTP service.'
# try:
#     smtp_service.send_email(recipient, email_subject, email_body)
# finally:
#     smtp_service.disconnect()   