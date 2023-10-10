import smtplib as s
import config_email

ob = s.SMTP("smtp.gmail.com",587)

ob.starttls()

ob.login(config_email.SENDER_MAIL,config_email.SENDER_MAIL_PASSWORD)

subject = ""