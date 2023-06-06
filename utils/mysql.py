import os
from typing import Tuple

import pymysql
from dotenv import load_dotenv

from utils.logger import get_logger


def mysql_connect():
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        database=os.getenv('DB_NAME'),
        passwd=os.getenv('DB_PASSWORD')
    )
    return conn


def insert_data_into_table(table_name: str, data: Tuple) -> None:
    """Insert data into a table.
    :param table_name: tables name for insert values
    :param data: data to write to the table
    """

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")  # select columns name from table
    col_names = [i[0] for i in cursor.description]

    try:
        guery_insert_data = f"""
            INSERT INTO {table_name}
                ({', '.join(col_names)})
                VALUES ({', '.join(['%s'] * len(col_names))});
        """
        cursor.executemany(guery_insert_data, [data])
        conn.commit()
        logger.info(f'Inserting values {data} into a table {table_name} completed successfully')
    except Exception as ex:
        logger.error(f'Some error occurred: {ex}')
        conn.rollback()
        raise ex


load_dotenv()
conn = mysql_connect()
cursor = conn.cursor()
logger = get_logger()
