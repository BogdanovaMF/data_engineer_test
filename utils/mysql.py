import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def mysql_connect():
    conn = pymysql.connect(
        host='localhost',
        user='dba',
        database='mysql',
        passwd='dbaPass'
    )
    return conn



