import os
from datetime import date

import requests
from dotenv import load_dotenv

from utilities import get_logger
from create_connect import get_mysql_connection


load_dotenv()

conn = get_mysql_connection()
cursor = conn.cursor()

logger = get_logger()


def get_data_usd_every_day(url: str):
    """Getting data usd on exchange rates every day
    :param url: link to get data on exchange rates
    """
    responce = requests.get(url).json()
    currencies = responce['quotes']
    id_currencies = {'RUB': currencies['USDRUB'], 'EUR': currencies['USDEUR'], 'CNY': currencies['USDCNY']}

    for id_curr in id_currencies:
        logger.info('Data received successfully')
        try:
            query = f"""INSERT INTO stage_currencies
                            (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                        values ("{date.today()}", "{id_curr}", "USD", {id_currencies[id_curr]}, "currencylayer");"""
            cursor.execute(query)
        except Exception as ex:
            logger.error(f'Error: {ex}')

    try:
        query_rub = f"""INSERT INTO stage_currencies
                        (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                        values ("{date.today()}", "USD", "USD", 1, "currencylayer")"""
        cursor.execute(query_rub)
        conn.commit()
    except Exception as ex:
        logger.error(f'Error: {ex}')


if __name__ == '__main__':
    api = os.getenv('API')
    url = f'http://apilayer.net/api/live?access_key={api}&currencies=RUB,EUR,CNY&source=USD&format=1'
    get_data_usd_every_day(url=url)
