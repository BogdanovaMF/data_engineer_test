import os
import time
from datetime import date, timedelta

import currencylayer
from dotenv import load_dotenv

from utils import get_logger
from create_connect1 import get_mysql_connection

conn = get_mysql_connection()
cursor = conn.cursor()

logger = get_logger()

load_dotenv()


def get_data_insert_to_db(days: int):
    """Getting data for several days and database entry
    :param days: amount of days
    """
    for day in range(days):
        historic_date = date.today() - timedelta(days=day)
        date_str = historic_date.strftime('%Y-%m-%d')

        exchange_rate = currencylayer.Client(access_key=os.getenv('API'))
        data = exchange_rate.historical(date=date_str, base_currency='USD')
        currencies = data['quotes']
        time.sleep(1)
        RUB = currencies['USDRUB']
        EUR = currencies['USDEUR']
        CNY = currencies['USDCNY']
        id_currencies = {'USDRUB': RUB, 'USDEUR': EUR, 'USDCNY': CNY}
        for id_curr in id_currencies:
            value = id_currencies[id_curr]
            try:
                query = f"""INSERT INTO stage_currencies
                                            (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                                            values ("{historic_date}", "{id_curr}", "USD", {value}, "currencylayer");"""
                cursor.execute(query)
            except Exception as ex:
                logger.error(f'Error: {ex}')

            logger.info('Data received successfully')
        try:
            query_rub = f"""INSERT INTO stage_currencies
                                (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                                values ("{historic_date}", "USD", "USD", 1, "currencylayer")"""
            cursor.execute(query_rub)
            conn.commit()
        except Exception as ex:
            logger.error(f'Error: {ex}')


if __name__ == '__main__':
    get_data_insert_to_db(365)
