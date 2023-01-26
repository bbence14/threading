import threading
import requests
from lxml import html
import time
import random


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            val = self._input_queue.get()
            if val == 'DONE':
                break

            yahooFinanceWorker = YahooFinanceWorker(symbol=val)
            price = yahooFinanceWorker.get_price()
            print(price)
            time.sleep(random.random())


class YahooFinanceWorker:
    def __init__(self, symbol):
        self.symbol = symbol
        _base_url = 'https://finance.yahoo.com/quote/'
        self._url = f"{_base_url}{self.symbol}"

    def get_price(self):
        time.sleep(30 * random.random())
        r = requests.get(self._url)
        if r.status_code != 200:
            return
        page_contents = html.fromstring(r.text)
        raw_price = page_contents.xpath(page_contents.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div[1]/fin-streamer[1]')[0].text)
        price = float(raw_price.replace(',', ''))
        return price
