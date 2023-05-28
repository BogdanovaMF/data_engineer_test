import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def mysql_connect():
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        database=os.getenv('DB_NAME'),
        passwd=os.getenv('DB_PASSWORD')
    )
    return conn



