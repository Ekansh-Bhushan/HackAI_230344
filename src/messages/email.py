import smtplib as s
import config_email

ob = s.SMTP("smpt.gmail.com",578)

ob.starttls()

ob.login