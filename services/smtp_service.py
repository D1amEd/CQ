import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class GmailSMTPService:
    def __init__(self, email_address: str, password: str):
        """
        Initialize the Gmail SMTP service with user credentials.
        """
        self.email_address = email_address
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587  # TLS port
        self.connection = None

    def connect(self):
        """
        Connect to the Gmail SMTP server and log in.
        """
        try:
            self.connection = smtplib.SMTP(self.server, self.port)
            self.connection.ehlo()
            self.connection.starttls()
            self.connection.login(self.email_address, self.password)
            print("Connected to Gmail SMTP server successfully.")
        except Exception as e:
            print("Failed to connect to the Gmail SMTP server:", e)
            raise

    def send_email(self, to_email: str, subject: str, message: str):
        """
        Send an email with the given subject and message to the specified recipient.
        """
        # Establish connection if not already done
        if self.connection is None:
            self.connect()

        # Set up the MIME message
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            self.connection.send_message(msg)
            print(f"Email sent successfully to {to_email}.")
        except Exception as e:
            print("Failed to send email:", e)
            raise

    def disconnect(self):
        """
        Disconnect from the Gmail SMTP server.
        """
        if self.connection:
            self.connection.quit()
            self.connection = None
            print("Disconnected from Gmail SMTP server.")