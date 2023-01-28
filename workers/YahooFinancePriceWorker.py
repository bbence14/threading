import threading
import time
import datetime
import random
from queue import Empty

import requests
from lxml import html


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        self._output_queue = temp_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._input_queue.get()
            except Empty:
                print('Yahoo scheduler queue is empty')
                break
            if val == 'DONE':
                for output_queue in self._output_queue:
                    output_queue.put('DONE')
                break

            yahooFinanceWorker = YahooFinanceWorker(symbol=val)
            price = yahooFinanceWorker.get_price()
            for output_queue in self._output_queue:
                output_values = (val, price, datetime.datetime.utcnow())
                output_queue.put(output_values)
            print(price)
            print(self._output_queue)
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
        price = float(str(raw_price).replace(',', ''))
        return price
