from utils import get_logger
from create_connect1 import get_mysql_connection

conn = get_mysql_connection()
cursor = conn.cursor()

logger = get_logger()


def insert_to_core(table_name_to: str, table_name_from):
    """Inserting data into core from staging
    :param table_name_to: table names to retrieve data
    :param table_name_from: staging table
    """
    query = f"""
        INSERT INTO {table_name_to} 
            (date, source, abbreviation1, abbreviation2, exchange_rate)
        SELECT pub_date,source, abbreviation1, abbreviation2, extrange_rate 
        FROM {table_name_from};
        """
    cursor.execute(query)
    conn.commit()


def update_core(table_name: str):
    """Updating data into core from staging
    :param table_name: table names to retrieve data
    """
    queries = f"""
        UPDATE {table_name} SET source_id=2 WHERE source='currencylayer';
        UPDATE {table_name} SET source_id=1 WHERE source='ЦБР';
        UPDATE {table_name} SET language_id=1 WHERE abbreviation1='USD';
        UPDATE {table_name} SET language_id=2 WHERE abbreviation1='RUB';
        UPDATE {table_name} SET language_id=4 WHERE abbreviation1='EUR';
        UPDATE {table_name} SET language_id=3 WHERE abbreviation1='CNY';
    """
    cursor.execute(queries)
    conn.commit()
