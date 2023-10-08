import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Function to send email alerts
def send_email_alert(receiver_email, subject, message):
    # Replace with your SMTP server details
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'
    
    # Create a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    
    # Create an email message
    email_message = MIMEMultipart()
    email_message['From'] = smtp_username
    email_message['To'] = receiver_email
    email_message['Subject'] = subject
    
    # Add the message body
    email_message.attach(MIMEText(message, 'plain'))
    
    # Send the email
    server.sendmail(smtp_username, receiver_email, email_message.as_string())
    
    # Close the SMTP server connection
    server.quit()

# Example usage with random input values
if __name__ == '__main__':
    # Generate a random email address for testing
    random_email = f'user{random.randint(1, 100)}@example.com'
    subject = 'Currency Exchange Rate Alert'
    message = 'The exchange rate has crossed your defined threshold.'
    
    try:
        send_email_alert(random_email, subject, message)
        print(f'Alert email sent to {random_email}')
    except Exception as e:
        print(f'Error sending email: {str(e)}')
