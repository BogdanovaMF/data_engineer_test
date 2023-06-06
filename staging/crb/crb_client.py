import argparse
from typing import Optional, Dict
from datetime import datetime, date

import requests
import pandas as pd
from parsel import Selector
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


class CrbClient:
    """Class for getting the exchange rate from https://www.cbr.ru/"""
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    source_code = 'ЦБ РФ'

    def __init__(self, conn: Optional[Connection]):
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    def parse_and_save(self, date: str, currency_codes: Dict, table_name: str) -> None:
        """Parsing data from the site and saving to the database
         :param date: currency conversion date
         :param currency_codes: dict with currencies id and currencies code
         :param table_name: tables name for insert values
         """
        currencies = self._request_and_parse(date, currency_codes)
        date = datetime.strptime(date, "%d/%m/%Y").date()
        for curr in currencies:
            data = (date, curr, "RUB", currencies[curr], self.source_code, datetime.now())
            insert_data_into_table(table_name, data)

    def _request_and_parse(self, date: str, currency_codes: Dict) -> Dict:
        """Parsing data from the site
        :param date: currency conversion date
        :param currency_codes: dict with currencies id and currencies code
        :return: dict with currency id and currency rate
        """
        try:
            response = requests.get(self.url.format(date=date))
            content = response.content.decode('cp1251', errors='ignore')
            html_sel = Selector(content).xpath('//html')[0]
            exchange_rates = {}
            for code, id in currency_codes.items():
                value = html_sel.xpath(f'//valute[contains(@id, "{id}")]/value//text()').get()
                value = float(value.replace(',', '.'))
                logger.info(f'{currency_codes[code]} exchange rate = {value}')
                exchange_rates[code] = value
            return exchange_rates

        except Exception as ex:
            logger.error(f'Some error occurred: {ex}')
            raise ex


if __name__ == '__main__':
    args = parse_args()
    logger = get_logger()

    crb = CrbClient(conn=mysql_connect())
    currency_codes = {
        'USD': 'R01235',
        'EUR': 'R01239',
        'CNY': 'R01375',
        }

    if args['date_from'] is None and args['date_to'] is None:
        date_str = date.today().strftime('%d/%m/%Y')
        crb.parse_and_save(date_str, currency_codes, args['table_name'])

    else:
        daterange = pd.date_range(start=args['date_from'], end=args['date_to'])
        for date in daterange:
            date_str = date.strftime('%d/%m/%Y')
            crb.parse_and_save(date_str, currency_codes, args['table_name'])