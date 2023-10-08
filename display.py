import requests

# Define your API key from exchangeratesapi.io
api_key = "YOUR_API_KEY_HERE"

# Function to convert currency using the API
def convert_currency(currency_name, currency_value, preferred_currency):
    # Build the URL for the API request
    base_url = "https://api.apilayer.com/exchangerates_data/latest"
    params = {
        "access_key": api_key,
        "base": currency_name,
        "symbols": preferred_currency
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200 and 'rates' in data:
            exchange_rate = data['rates'][preferred_currency]
            converted_value = currency_value * exchange_rate
            return converted_value
        else:
            return "Error: Unable to fetch exchange rates from the API"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Input currency name, value, and preferred currency
currency_name = input("Enter the currency name (e.g., USD, EUR, GBP): ").upper()
currency_value = float(input("Enter the currency value: "))
preferred_currency = input("Enter the preferred currency (e.g., USD, EUR, GBP): ").upper()

# Convert and display the result
converted_value = convert_currency(currency_name, currency_value, preferred_currency)
if isinstance(converted_value, str):
    print(converted_value)
else:
    print(f"{currency_value} {currency_name} is equivalent to {converted_value:.2f} {preferred_currency}")

