from typing import Dict
from datetime import date

from utilities import get_logger, get_values
from create_connect import get_mysql_connection


conn = get_mysql_connection()
cursor = conn.cursor()

logger = get_logger()


def get_data_every_day(id_currencies: Dict):
    """Getting data on exchange rates every day
    :param id_currencies: currencies id to get the rate
    """
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='
    today_date = date.today()
    str_date = today_date.strftime('%d/%m/%Y')
    source = url + str_date
    for id_curr in id_currencies:
        value = get_values(source, id_currencies[id_curr])
        logger.info('Data received successfully')
        try:
            query = f"""INSERT INTO stage_currencies
                                    (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                                    values ("{today_date}", "{id_curr}", "RUB", {value}, "ЦБР");"""
            cursor.execute(query)
        except Exception as ex:
            logger.error(f'Error: {ex}')

    try:
        query_rub = f"""INSERT INTO stage_currencies
                        (pub_date, abbreviation1, abbreviation2, extrange_rate, source)
                        values ("{today_date}", "RUB", "RUB", 1, "ЦБР")"""
        cursor.execute(query_rub)
        conn.commit()
    except Exception as ex:
        logger.error(f'Error: {ex}')


if __name__ == '__main__':
    currencies_id = {
        'USD': 'R01235',
        'EUR': 'R01239',
        'CNY': 'R01375',
    }
    get_data_every_day(currencies_id)