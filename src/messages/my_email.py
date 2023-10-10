
import os
from email.message import EmailMessage
import ssl
import smtplib
import config_email

"""ob = s.SMTP("smtp.gmail.com",587)

ob.starttls()

ob.login(config_email.SENDER_MAIL,config_email.SENDER_MAIL_PASSWORD)

subject = "Alert : The currency rate is gone below/above the threshold value."

body = "Please check the values on the app."

message = "Subject:{}\n\n{}".format(subject,body)

print(message)
"""
SENDER_MAIL=""
RECIEVER_MAIL=""
SENDER_MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SUBJECT='CHECK OUT MY NEW VIDEO'
BODY='PUBLISHED A VIDEO ON YOUTUBE'
APP_PASSWORD = "lunw obce mucm mcga" 

em=EmailMessage()
em['From']=SENDER_MAIL
em['To']=RECIEVER_MAIL
em['Subject']=SUBJECT
em.set_content(BODY)

context=ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(SENDER_MAIL,SENDER_MAIL_PASSWORD)
    smtp.sendmail(SENDER_MAIL,RECIEVER_MAIL,em.as_string())
 