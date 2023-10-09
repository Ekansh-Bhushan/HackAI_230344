import requests
from datetime import datetime

class Currency:
    def __init__(self):
        self.api_key = open('api_key.txt').readline().strip()
        self.url = f'http://api.exchangeratesapi.io/v1/latest?access_key={self.api_key}'
        # self.url = f'http://api.exchangeratesapi.io/v1/latest?access_key={self.api_key}&base=USD&symbols=GBP,EUR'
        self.output = ''
        self.file_name = datetime.now().strftime('%d %b - %Y')
        print(self.file_name)

    def do_request(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            res_json = res.json()
            self.output = res_json['rates']['USD']
            # print(self.output['rates']['USD'])
            print(self.output)

    def write_to_file(self):
        tday = datetime.now().strftime('%Y-%m-%d')
        temp_dict = {tday: self.output}
        with open(f"daily_price/{self.file_name}", 'w') as f :
            json.dump(temp_dict, f)
        # print(self)

c = Currency()
c.do_request()