import requests
from datetime import datetime
import json
import csv
from src.utilis.userDatabase import send_user_currency,send_user_threshold
from src.messages.my_email import send_mail_to_user

from uagents import Agent, Context

# from uagents import Agent, Context

class Currency:
    def __init__(self):
        self.api_key = open('src/agents/currency/api_key.txt').readline().strip()
        self.url = f'http://api.exchangeratesapi.io/v1/latest?access_key={self.api_key}'
        # self.url = f'http://api.exchangeratesapi.io/v1/latest?access_key={self.api_key}&base=USD&symbols=GBP,EUR'
        self.output = ''
        self.file_name = datetime.now().strftime('%d %b - %Y')
        print(self.file_name)


    def do_request(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            res_json = res.json()
            self.output = res_json['rates']
            return self.output
    
    def write_to_file(self):
        tday = datetime.now().strftime('%Y-%m-%d')
        # print(tday)
        temp_dict = {tday: self.output}
        with open(f"daily_price/{self.file_name}.txt", 'w') as f :
            json.dump(temp_dict, f)
        # print(self)

    
# agent.run()

def currency_rate_get():

    c = Currency()
    global dicti 
    dicti = c.do_request()
    # c.write_to_file()
    # dicti = {}
    return dicti
api_threshold = currency_rate_get()
threshold =send_user_threshold()
currency = send_user_currency()

def is_valid_currency_name(curreny):
    # Check if the currency code is in the dictionary
    return currency in dicti

def get_currency_key(currency):
    # Return the key (acronym) for a given currency value
    for key, value in dicti.items():
        if value == currency:
            return key
    return None
def sending_alert(curreny):
    
    agent= Agent(name="agent", seed="agent recovery phase")
    @agent.on_interval(period=84600) #update in a day
    async def currency_update(ctx: Context):
        ctx.logger.info(f'The current rate today is ')
    curreny_from_database = is_valid_currency_name(curreny)
    currency_key_from_database = get_currency_key(curreny)
    try:
        if threshold <api_threshold:
            send_mail_to_user()
    except Exception as e:
        print(e)


