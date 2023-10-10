import csv
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # Import MIMEMultipart for sending emails
from database import get_email  # Import the function from your database.py

# Define your API endpoint and API key
api_key = open('api_key.txt').readline().strip()
api_url = f'http://api.exchangeratesapi.io/v1/latest?access_key={api_key}'  # Move the API URL after defining api_key

# Define the base currency (EUR)
base_currency = 'EUR'

# Specify the file path to your CSV file
csv_file_path = 'exchangerates.csv'

try:
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)  # Use DictReader to read CSV as a dictionary
        for row in reader:
            # Access values by column name (header)
            currency_code = row['Currency Code']
            threshold = float(row['Threshold'])  # Convert threshold to float
            email_address = row['Email Address']
            # Print or process these values as needed
            print(f"Currency Code: {currency_code}, Threshold: {threshold}, Email Address: {email_address}")
    print("CSV file has been successfully read.")
except FileNotFoundError:
    print(f"The file '{csv_file_path}' was not found.")
except Exception as e:
    print(f"An error occurred while reading the file '{csv_file_path}': {e}")

# Function to fetch exchange rates from the API
def get_exchange_rates():
    params = {
        'base': base_currency,
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data['rates']
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch exchange rates from the API: {e}")
        return None

# Function to send email alerts
def send_alert(email_address, currency_code, exchange_rate, threshold):
    subject = f'Currency Alert: {currency_code} Exceeds Threshold'
    message = f'The exchange rate for {currency_code} has exceeded your set threshold. Current rate: {exchange_rate}, Threshold: {threshold}'
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'your_email@gmail.com'  # Replace with your email address
    msg['To'] = email_address
    
    # Create a plain text message
    text_message = MIMEText(message)
    msg.attach(text_message)
    
    smtp_server = 'smtp.gmail.com'  # Use your SMTP server
    smtp_port = 587  # Use your SMTP port
    smtp_username = 'your_email@gmail.com'  # Replace with your email address
    smtp_password = 'your_email_password'  # Replace with your email password
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, email_address, msg.as_string())
        server.quit()
        print(f"Alert sent to {email_address} for {currency_code}.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email alert to {email_address}: {e}")

# Main function
def main():
    exchange_rates = get_exchange_rates()
    
    if exchange_rates is None:
        print("Exiting due to API request error.")
        return
    
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            currency_code = row['Currency Code']
            threshold = float(row['Threshold'])
            email_address = row['Email Address']
            
            if currency_code in exchange_rates:
                exchange_rate = exchange_rates[currency_code]
                
                if exchange_rate > threshold:
                    send_alert(email_address, currency_code, exchange_rate, threshold)

if __name__ == '__main__':
    print("Currency exchange monitor started.")
    main()
    print("Currency exchange monitor finished.")





