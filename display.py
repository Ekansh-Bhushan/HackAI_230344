#this is the display file
import requests

def get_exchange_rate(base_currency, target_currency):
    # Replace with the URL of the currency exchange rate API
    api_url = f"https://api.exchangeratesapi.io/latest?base={base_currency}"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if target_currency in data["rates"]:
            exchange_rate = data["rates"][target_currency]
            return exchange_rate
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rate: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    base_currency = "USD"
    target_currency = "EUR"
    
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    
    if exchange_rate is not None:
        print(f"Exchange rate from {base_currency} to {target_currency}: {exchange_rate}")
    else:
        print(f"Unable to fetch the exchange rate for {base_currency} to {target_currency}")
