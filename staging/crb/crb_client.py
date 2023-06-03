import requests
import argparse

from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta, date

import pandas as pd
from pymysql import Connection
from bs4 import BeautifulSoup as bs

from utils.logger import get_logger
from utils.mysql import mysql_connect


def parse_args():
    """Getting  data from the user from the command line for searching"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--date_from')
    parser.add_argument('--date_to')
    parser.add_argument('--table', required=True)
    args = parser.parse_args()
    return vars(args)


class CrbClient:
    """Class for getting the exchange rate from https://www.cbr.ru/"""
    URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    source = 'ЦБ РФ'

    def __init__(self, conn: Optional[Connection]):
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    def parse_and_save(self, date: str, currencies_id: Dict, table_name: str) -> None:
        """Parsing data from the site and saving to the database
         :param date: currency conversion date
         :param currencies_id: dict with currencies id and currencies code
         :param table_name: tables name for insert values
         """
        currencies = self._request_and_parse(date, currencies_id)
        date = datetime.strptime(date, "%d/%m/%Y").date()
        for curr in currencies:
            data = (date, curr, "RUB", currencies[curr], self.source, datetime.now())
            self.insert_data_into_table(table_name, data)

    def _request_and_parse(self, date: str, currencies_id: Dict) -> Dict:
        """Parsing data from the site
        :param date: currency conversion date
        :param currencies_id: dict with currencies id and currencies code
        :return: dict with currency id and currency rate
        """
        try:
            response = requests.get(self.URL.format(date=date))
            content = response.text
            soup = bs(content, features="xml")
            curr_new = {}
            for code in currencies_id:
                value = float(soup.find('Valute', {'ID': currencies_id[code]}).find('Value').get_text().replace(',', '.'))
                logger.info(f'{currencies_id[code]} exchange rate = {value}')
                curr_new[code] = value
            return curr_new

        except Exception as ex:
            logger.error(f'Some error occurred: {ex}')

    def insert_data_into_table(self, table_name: str, data: Tuple) -> None:
        """Insert data into a table.
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

    crb = CrbClient(conn=mysql_connect())
    currencies_id = {
        'USD': 'R01235',
        'EUR': 'R01239',
        'CNY': 'R01375',
        }

    if args['date_from'] is None and args['date_to'] is None:
        historic_date = date.today() - timedelta(days=0)
        date_str = historic_date.strftime('%d/%m/%Y')
        crb.parse_and_save(date_str, currencies_id, args['table'])

    else:
        daterange = pd.date_range(start=args['date_from'], end=args['date_to'])
        for date in daterange:
            date_str = date.strftime('%d/%m/%Y')
            crb.parse_and_save(date_str, currencies_id, args['table'])