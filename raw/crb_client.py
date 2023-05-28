import argparse
import requests
from typing import Optional, Tuple
from datetime import date, timedelta

from pymysql import Connection
from bs4 import BeautifulSoup as bs

from utils.logger import get_logger
from utils.mysql import mysql_connect

logger = get_logger()


def parse_args():
    """Getting  data from the user from the command line for searching"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', required=True)
    parser.add_argument('--table', required=True)
    args = parser.parse_args()
    return vars(args)


class CrbClient:
    URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="

    def __init__(self, conn: Optional[Connection]):
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    def parse_and_save(self, date, id_currencies):
        """запись и сохранение в дб"""
        date_str = date.strftime('%d/%m/%Y')
        source_url = self.URL + date_str
        value = self._request_and_parse(source_url, id_currencies)
        logger.info('Data received successfully')
        return value

    @staticmethod
    def _request_and_parse(url: str, currencies_id) -> float:
        try:
            response = requests.get(url, timeout=5)
            currency_content = response.text
            soup = bs(currency_content, features="xml")
            value = float(soup.find('Valute', {'ID': currencies_id}).find('Value').get_text().replace(',', '.'))

            return value

        except requests.RequestException as ex:
            logger.error(f'Error: {ex}')

    def insert_data_into_table(self, table_name: str, data: Tuple) -> None:
        """Create temp table. Insert data into a table.
        :param table_name: tables name for insert values
        :param data: data to write to the table
        """

        self.cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")  # select columns name from table
        col_names = [col.name for col in self.cursor.description if col.name != 'id']  # identified columns without id
        try:
            guery_insert_data = f"""
                INSERT INTO {table_name} 
                    ({', '.join(col_names)})
                VALUES ({', '.join(['%s'] * len(col_names))});
            """
            self.cursor.executemany(guery_insert_data, data)
            self.conn.commit()
            logger.info(f'Inserting values into a table {table_name} completed successfully')
        except Exception as ex:
            logger.error(f'Some error occurred: {ex}')
            self.conn.rollback()
            raise ex


if __name__ == '__main__':
    args = parse_args()

    currencies_id = {
        'USD': 'R01235',
        'EUR': 'R01239',
        'CNY': 'R01375',
    }

    crb = CrbClient(conn=mysql_connect())
    for day in range(args['days']):
        historic_date = date.today() - timedelta(days=day)
        for curr in currencies_id:
            value = crb.parse_and_save(historic_date, currencies_id[curr])
            data = (date.today(), curr, "RUB", {value}, "ЦБР")
            crb.insert_data_into_table(args['table'], data)
        data2 = (historic_date, "RUB", "RUB", 1, "ЦБР")
        crb.insert_data_into_table(args['table'], data2)
