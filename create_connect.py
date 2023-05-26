import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_mysql_connection():
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        database=os.getenv('DB_NAME'),
        passwd=os.getenv('DB_PASSWORD')
    )
    return conn
