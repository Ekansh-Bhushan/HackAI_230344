
import os
from email.message import EmailMessage
import ssl
import smtplib
import config_email
from src.utilis.userDatabase import user_email

mail = user_email()


SENDER_MAIL_PASSWORD = os.environ.get(config_email.SENDER_MAIL_PASSWORD)
SUBJECT='Alert : The currency rate is gone below/above the threshold value.'
BODY='lease check the values on the app.'
APP_PASSWORD = config_email.APP_PASSWORD

em=EmailMessage()
em['From']=config_email.SENDER_MAIL
em['To']=mail
em['Subject']=SUBJECT
em.set_content(BODY)

def send_mail_to_user():
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(config_email.SENDER_MAIL,config_email.SENDER_MAIL_PASSWORD)
        smtp.sendmail(config_email.SENDER_MAIL,mail,em.as_string())
    