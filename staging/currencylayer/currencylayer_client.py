import os
import time
import argparse
from datetime import datetime, date
from typing import Optional, Dict, List

import pandas as pd
import currencylayer
from dotenv import load_dotenv
from pymysql import Connection

from utils.logger import get_logger
from utils.mysql import mysql_connect, insert_data_into_table


def parse_args():
    """Getting  data from the user from the command line for searching"""
    parser = argparse.ArgumentParser(description='Getting the range of dates for currency conversion and the name of '
                                                 'the table in which the data on exchange rates will be entered')
    parser.add_argument('--date_from', help='starting date from which exchange rate information will be collected')
    parser.add_argument('--date_to', help='end date from which exchange rate information will be collected')
    parser.add_argument('--table_name', required=True, help='tables name for insert values')
    args = parser.parse_args()
    return vars(args)


class CurrencylayerClient:
    """Class for getting the exchange rate from https://currencylayer.com/"""
    source_code = 'currencylayer'

    def __init__(self, conn: Optional[Connection]):
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    def parse_and_save(self, date: str, currency_codes: List, table_name: str) -> None:
        """Parsing data from the site and saving to the database
         :param date: currency conversion date
         :param currency_codes: list with currencies codes
         :param table_name: tables name for insert values
         """
        currencies = self._request_and_parse(date, currency_codes)
        for curr in currencies:
            value = currencies[curr]
            data = (date, curr, "USD", value, self.source_code, datetime.now())
            insert_data_into_table(table_name, data)

    @staticmethod
    def _request_and_parse(date: str, currency_codes: List) -> Dict:
        """Parsing data from the site
        :param date: exchange rate conversion date
        :param currency_codes: list with currencies code
        :return: dict with currency id and currency rate
        """
        try:
            exchange_rates = {}
            exchange_rate = currencylayer.Client(access_key=os.getenv('API'))
            data = exchange_rate.historical(date=date, base_currency="USD")
            currencies = data['quotes']
            for i in currency_codes:
                value = currencies[i]
                exchange_rates[i[3:]] = value
                logger.info(f'From {i[:3]} to {i[3:]} exchange rate = {value}')

            return exchange_rates

        except Exception as ex:
            logger.error(f'Error: {ex}')
            raise ex


if __name__ == '__main__':
    args = parse_args()
    logger = get_logger()
    load_dotenv()
    curr_layer = CurrencylayerClient(conn=mysql_connect())
    currency_codes = ['USDRUB', 'USDEUR', 'USDCNY']

    if args['date_from'] is None and args['date_to'] is None:
        date_str = date.today().strftime('%Y-%m-%d')
        curr_layer.parse_and_save(date_str, currency_codes, args['table_name'])

    else:
        daterange = pd.date_range(start=args['date_from'], end=args['date_to'])
        for date in daterange:
            date_str = date.strftime('%Y-%m-%d')
            curr_layer.parse_and_save(date_str, currency_codes, args['table_name'])
            time.sleep(1)
