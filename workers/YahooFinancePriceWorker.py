import threading
import requests
from lxml import html
import time
import random


class YahooFinanceWorker(threading.Thread):
    def __init__(self, symbol, **kwargs):
        super(YahooFinanceWorker, self).__init__(**kwargs)
        self.symbol = symbol
        _base_url = 'https://finance.yahoo.com/quote/'
        self._url = f"{_base_url}{self.symbol}"
        self.start()

    def run(self):
        time.sleep(30 * random.random())
        r = requests.get(self._url)
        if r.status_code != 200:
            return
        page_contents = html.fromstring(r.text)
        price = float(page_contents.xpath(page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text))
        print(price)
