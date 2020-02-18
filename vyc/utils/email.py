from voiceYourConcern.settings import SENDGRID_KEY
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(from_email,to,subject,content):
    message = Mail(
        from_email=from_email,
        to_emails=to,
        subject=subject,
        html_content=content)

    sg = SendGridAPIClient(SENDGRID_KEY)
    response = sg.send(message)
