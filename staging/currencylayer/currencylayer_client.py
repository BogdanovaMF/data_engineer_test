import os
import argparse
from datetime import datetime, date, timedelta
from typing import Optional, Dict, List, Tuple

import currencylayer
from dotenv import load_dotenv
from pymysql import Connection

from utils.logger import get_logger
from utils.mysql import mysql_connect


def parse_args():
    """Getting  data from the user from the command line for searching"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', required=True)
    parser.add_argument('--table', required=True)
    args = parser.parse_args()
    return vars(args)


class CurrencylayerClient:
    """Class for getting the exchange rate from https://currencylayer.com/"""
    source = 'currencylayer'

    def __init__(self, conn: Optional[Connection]):
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    def parse_and_save(self, date: str, currencies_id: List, table_name: str) -> None:
        """Parsing data from the site and saving to the database
         :param date: currency conversion date
         :param currencies_id: list with currencies id
         :param table_name: tables name for insert values
         """
        currencies = self._request_and_parse(date, currencies_id)
        for curr in currencies:
            value = currencies[curr]
            data = (date, curr, "USD", value, self.source, datetime.now())
            self.insert_data_into_table(table_name, data)

    @staticmethod
    def _request_and_parse(date: str, curr_from_to: List) -> Dict:
        """Parsing data from the site
        :param date: exchange rate conversion date
        :param curr_from_to: list with currencies id
        :return: currency values dict
        """
        try:
            id_currencies = {}
            exchange_rate = currencylayer.Client(access_key=os.getenv('API'))
            data = exchange_rate.historical(date=date, base_currency="USD")
            currencies = data['quotes']
            for i in curr_from_to:
                value = currencies[i]
                id_currencies[i[3:]] = value
                logger.info(f'From {i[:3]} to {i[3:]} exchange rate = {value}')

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
            logger.info(f'Inserting values {data} into a table {table_name} completed successfully')
        except Exception as ex:
            logger.error(f'Some error occurred: {ex}')
            self.conn.rollback()
            raise ex


if __name__ == '__main__':
    args = parse_args()
    logger = get_logger()
    load_dotenv()
    curr_layer = CurrencylayerClient(conn=mysql_connect())
    currencies_id = ['USDRUB', 'USDEUR', 'USDCNY']

    for day in range(int(args['days'])):
        historic_date = date.today() - timedelta(days=day)
        date_str = historic_date.strftime('%Y-%m-%d')
        curr_layer.parse_and_save(date_str, currencies_id, 'stage_currencies')
