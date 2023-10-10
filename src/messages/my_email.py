import smtplib as s
import config_email

ob = s.SMTP("smtp.gmail.com",587)

ob.starttls()

ob.login(config_email.SENDER_MAIL,config_email.SENDER_MAIL_PASSWORD)

subject = "Alert : The currency rate is gone below/above the threshold value."

body = "Please check the values on the app."

message = "Subject:{}\n\n{}".format(subject,body)

print(message)