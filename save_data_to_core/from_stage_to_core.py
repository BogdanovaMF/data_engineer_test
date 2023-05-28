from utils.logger import get_logger
from utils.mysql import mysql_connect

conn = mysql_connect()
cursor = conn.cursor()

logger = get_logger()


def insert_to_core(table_name_to: str, table_name_from):
    """Inserting data into core from staging
    :param table_name_to: table names to retrieve data
    :param table_name_from: staging table
    """
    try:
        query = f"""
            INSERT INTO {table_name_to} 
                (exchange_date, source_id, currency_source_id, currency_destination_id, exchange_rate, load_rout_timestamp)
            SELECT exchange_date,source_id, currency_source_id, currency_destination_id, extrange_rate, load_rout_timestamp
            FROM {table_name_from};
            """
        cursor.execute(query)
        conn.commit()
        logger.info(f'Inserting values into a table {table_name_to} completed successfully')
    except Exception as ex:
        logger.error(f'Some error occurred: {ex}')
        conn.rollback()
        raise ex


def update_core(table_name: str):
    """Updating data into core from staging
    :param table_name: table names to retrieve data
    """
    try:
        queries = f"""
            UPDATE {table_name} SET language_id=1 WHERE currency_source_id='USD';
            UPDATE {table_name} SET language_id=2 WHERE currency_source_id='RUB';
            UPDATE {table_name} SET language_id=4 WHERE currency_source_id='EUR';
            UPDATE {table_name} SET language_id=3 WHERE currency_source_id='CNY';
        """
        cursor.execute(queries)
        conn.commit()
        logger.info(f'Updating values into a table {table_name} completed successfully')
    except Exception as ex:
        logger.error(f'Some error occurred: {ex}')
        conn.rollback()
        raise ex


if __name__ == '__main__':
    insert_to_core('stage_currencies', 'exchange_rates')
    update_core('exchange_rates')

