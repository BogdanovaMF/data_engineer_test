from typing import Dict
from datetime import date, timedelta

from utils import get_logger, get_values
from config import currencies_id, url
from create_connect import get_mysql_connection

conn = get_mysql_connection()
cursor = conn.cursor()

logger = get_logger()


def get_data_few_days(days: int, id_currencies: Dict):
    """Getting data for several days and database entry
    :param days: amount of days
    :param id_currencies: currencies id to get the rate
    """
    for day in range(days):
        historic_date = date.today() - timedelta(days=day)
        date_str = historic_date.strftime('%d/%m/%Y')
        source_url = url + date_str
        for id_curr in id_currencies:
            value = get_values(source_url, id_currencies[id_curr])
            logger.info('Data received successfully')
            try:
                query = f"""INSERT INTO stage_currencies
                            (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                            values ("{historic_date}", "{id_curr}", "RUB", {value}, "ЦБР");"""
                cursor.execute(query)
            except Exception as ex:
                logger.error(f'Error: {ex}')
        try:
            query_rub = f"""INSERT INTO stage_currencies
                            (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                            values ("{historic_date}", "RUB", "RUB", 1, "ЦБР")"""
            cursor.execute(query_rub)
            conn.commit()
        except Exception as ex:
            logger.error(f'Error: {ex}')


if __name__ == '__main__':
    get_data_few_days(365, currencies_id)

