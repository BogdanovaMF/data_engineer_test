import os
import argparse
from typing import Optional, Tuple, Dict
from datetime import date, timedelta, time, datetime

import currencylayer
from dotenv import load_dotenv
from pymysql import Connection

from utils.logger import get_logger
from utils.mysql import mysql_connect

logger = get_logger()
load_dotenv()


def parse_args():
    """Getting  data from the user from the command line for searching"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', required=True)
    parser.add_argument('--table', required=True)
    args = parser.parse_args()
    return vars(args)


class CurrencylayerClient:
    """Class for getting the exchange rate from https://currencylayer.com/"""
    def __init__(self, conn: Optional[Connection]):
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    @staticmethod
    def request_and_parse_history(historic_date: str) -> Dict:
        """Parsing data from the site
        :param historic_date: exchange rate conversion date
        :return: currency values dict
        """
        try:
            date_str = historic_date.strftime('%Y-%m-%d')

            exchange_rate = currencylayer.Client(access_key=os.getenv('API'))
            data = exchange_rate.historical(date=date_str, base_currency='USD')
            currencies = data['quotes']
            time.sleep(1)
            RUB = currencies['USDRUB']
            EUR = currencies['USDEUR']
            CNY = currencies['USDCNY']
            id_currencies = {'RUB': RUB, 'EUR': EUR, 'CNY': CNY}
            return id_currencies

        except Exception as ex:
            logger.error(f'Error: {ex}')

    def insert_data_into_table(self, table_name: str, data: Tuple) -> None:
        """Create temp table. Insert data into a table.
        :param table_name: tables name for insert values
        :param data: data to write to the table
        """

        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")  # select columns name from table
        col_names = [i[0] for i in self.cursor.description]

        try:
            guery_insert_data = f"""
                INSERT INTO {table_name}
                    ({', '.join(col_names)})
                    VALUES ({', '.join(['%s'] * len(col_names))});
            """
            self.cursor.executemany(guery_insert_data, [data])
            self.conn.commit()
            logger.info(f'Inserting values into a table {table_name} completed successfully')
        except Exception as ex:
            logger.error(f'Some error occurred: {ex}')
            self.conn.rollback()
            raise ex


if __name__ == '__main__':
    args = parse_args()

    curr_layer = CurrencylayerClient(conn=mysql_connect())

    for day in range(int(args['days'])):
        historic_date = date.today() - timedelta(days=day)
        currencies_id = curr_layer.request_and_parse_history(args['days'], historic_date)
        for curr in currencies_id:
            value = currencies_id[curr]
            data = (date.today(), curr, "USD", value, 2, datetime.now())
            curr_layer.insert_data_into_table(args['table'], data)
        data2 = (historic_date, "USD", "USD", 1, 2, datetime.now())
        curr_layer.insert_data_into_table(args['table'], data2)
