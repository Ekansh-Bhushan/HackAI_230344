import time
import requests
from uAgent import Agent, Rule, Task
from twilio.rest import Client  # You can replace this with your preferred notification method

# Define your currency exchange API endpoint and API key here
API_ENDPOINT = 'YOUR_API_ENDPOINT'
API_KEY = 'YOUR_API_KEY'

# Initialize the uAgent
agent = Agent("Currency Exchange Monitor")

# Define a function to fetch real-time exchange rates from the API
def fetch_exchange_rates(base_currency, foreign_currencies):
    params = {
        'base': base_currency,
        'symbols': ','.join(foreign_currencies),
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(API_ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        raise Exception("Failed to fetch exchange rates from the API")

# Define a function to send alerts (you can customize this for your preferred notification method)
def send_alert(alert_message):
    # Replace this with your notification method (e.g., Twilio, email, etc.)
    # Example using Twilio SMS:
    twilio_account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    twilio_auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    twilio_from_number = 'YOUR_TWILIO_PHONE_NUMBER'
    twilio_to_number = 'RECIPIENT_PHONE_NUMBER'
    
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        body=alert_message,
        from_=twilio_from_number,
        to=twilio_to_number
    )
    print(f"Alert sent: {message.sid}")

# Define a function to monitor exchange rates and send alerts
def monitor_exchange_rates(base_currency, foreign_currencies, thresholds):
    while True:
        try:
            rates = fetch_exchange_rates(base_currency, foreign_currencies)
            
            for currency, threshold in thresholds.items():
                if currency in rates:
                    rate = rates[currency]
                    if rate > threshold['upper']:
                        alert_message = f"Alert: {base_currency} to {currency} rate is above {threshold['upper']}"
                        send_alert(alert_message)
                    elif rate < threshold['lower']:
                        alert_message = f"Alert: {base_currency} to {currency} rate is below {threshold['lower']}"
                        send_alert(alert_message)
            time.sleep(60)  # Check rates every minute (adjust as needed)
        except Exception as e:
            print(f"Error: {str(e)}")

# Define the currencies to monitor and their thresholds
base_currency = 'USD'
foreign_currencies = ['INR', 'EUR']
thresholds = {
    'INR': {'upper': 82.60, 'lower': 82.55},
    'EUR': {'upper': 1.10, 'lower': 1.05},
}

# Create a task to monitor exchange rates
monitor_task = Task(
    monitor_exchange_rates,
    base_currency,
    foreign_currencies,
    thresholds
)

# Create a rule to run the monitor task
exchange_rate_rule = Rule("Exchange Rate Monitor", monitor_task)

# Add the rule to the agent
agent.add_rule(exchange_rate_rule)

# Start the agent
agent.start()
