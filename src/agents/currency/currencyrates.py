import requests
from datetime import datetime
import json
import csv
# from uagents import Agent, Context

# from uagents import Agent, Context

class Currency:
    def __init__(self):
        self.api_key = open('C:/Users/Ekansh/code/HackAI/src/agents/currency/api_key.txt').readline().strip()
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
    # agent= Agent(name="agent", seed="agent recovery phase")
    # @agent.on_interval(period=84600)
    # async def currency_update(ctx: Context):
    #     ctx.logger.info(f'The current rate today is {self.output}')
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