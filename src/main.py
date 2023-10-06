# import requests
# from bs4 import BeautifulSoup
# import smtplib
# import time

# def get_exchange_rates():
#     url = "https://your_currency_exchange_website.com"  # Replace with your currency exchange rate source
#     headers = {
#         "User-Agent": "Currency Exchange Monitor"
#     }

#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Parse the webpage and extract exchange rates
#     # Replace 'exchange_rate' with the appropriate HTML elements or classes
#     exchange_rate = soup.find('div', class_='exchange-rate').text.strip()
#     return float(exchange_rate)

# def send_email(subject, message):
#     sender_email = "your_email@gmail.com" # will be using backend in near future with the help of f string
#     sender_password = "your_email_password"
#     receiver_email = "receiver_email@gmail.com"

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)

#         email_message = f"Subject: {subject}\n\n{message}"
#         server.sendmail(sender_email, receiver_email, email_message)
#         print("Email sent successfully!")

#     except Exception as e:
#         print(f"Error sending email: {str(e)}")

# # Main function
# def main():
#     while True:
#         exchange_rate = get_exchange_rates()
        
#         # Set your desired conditions for sending an alert
#         if exchange_rate < 1.10:
#             subject = "Exchange Rate Alert"
#             message = f"Exchange rate is now {exchange_rate}. It's below your threshold."
#             send_email(subject, message)
        
#         # Set the polling interval (in seconds)
#         time.sleep(3600)  # Check every hour

# if __name__ == "__main__":
#     main()



