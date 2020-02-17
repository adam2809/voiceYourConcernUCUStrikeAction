from voiceYourConcern.settings import SENDGRID_KEY
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(from,to,subject,content):
    message = Mail(
        from_email=from,
        to_emails=to,
        subject=subject,
        html_content=content)

    sg = SendGridAPIClient(SENDGRID_KEY)
    response = sg.send(message)
