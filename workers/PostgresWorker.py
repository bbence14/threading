import os

import threading
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from queue import Empty


class PostgresMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        if 'output_queue' in kwargs:
            kwargs.pop('output_queue')
        super(PostgresMasterScheduler, self).__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._input_queue.get(timeout=10)
                print("PostgresStarted")
            except Empty as e:
                print('Timeout reached in postgres scheduler, stopping')
                break
            if val == 'DONE':
                break
            symbol, price, extracted_price = val
            postgresWorker = PostgresWorker(symbol, price, extracted_price)
            postgresWorker.insert_into_db()


class PostgresWorker:
    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        self._PG_USER = os.getenv('PGUSER')
        self._PG_PASSWORD = os.getenv('PGPASSWORD')
        self._HOST = os.getenv('PGHOST', 'localhost')
        self._PORT = os.getenv('PGPORT', '5432')
        self._PG_DATABASE = os.getenv('PGDATABASE')

        self._engine = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PASSWORD}@{self._HOST}:{self._PORT}/{self._PG_DATABASE}')

    def _create_insert_query(self):
        SQL = """ INSERT INTO prices (symbol, price, extracted_time) VALUES 
        (:symbol, :price, :extracted_time) """
        return SQL

    def insert_into_db(self):
        insert_query = self._create_insert_query()
        with self._engine.connect() as conn:
            conn.execute(text(insert_query), {'symbol': self._symbol,
                                              'price': self._price,
                                              'extracted_time': str(self._extracted_time)})

        with open('db.txt', 'a') as txt_writer:
            txt_writer.write(f"{self._symbol},'price': {self._price},'extracted_time': {str(self._extracted_time)}")

        print("Inserted successfully")




