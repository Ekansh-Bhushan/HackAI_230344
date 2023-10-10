import smtplib as s
import config_email

ob = s.SMTP("smpt.gmail.com",578)

ob.starttls()

ob.login(config_email.SENDER_MAIL,config_email.SENDER_MAIL_PASSWORD)

subject = ""