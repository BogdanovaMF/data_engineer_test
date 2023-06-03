from utils.logger import get_logger
from utils.mysql import mysql_connect

logger = get_logger()
conn = mysql_connect()
cursor = conn.cursor()


def create_table_dim(table_name: str, params_query: str):
    """Creating and entering data into the Data Marts table
    :param table_name: the name of the table to be created
    :param params_query: query parameters to create a table
    """
    try:
        query = f"""
            DROP TABLE IF EXISTS {table_name};
            CREATE TABLE as {table_name} {params_query};
        """
        cursor.execute(query)
        conn.commit()
        logger.info(f'Inserting values into a table {table_name} completed successfully')
    except Exception as ex:
        logger.error(f'Some error occurred: {ex}')
        conn.rollback()
        raise ex


if __name__ == "__main__":
    param_dim_currencies = f"""
            SELECT 
            exchange_date, language_id, currency_source_id, currency_destination_id, exchange_rate, load_rout_timestamp, source_id
            FROM exchange_rates
        """

    param_dim_currencies_rus = """
            SELECT 
            exchange_date, curr_name_rus, currency_source_id, currency_destination_id, exchange_rate, load_rout_timestamp, source_id
            FROM exchange_rates AS t1
            INNER JOIN languages as t2 
            ON t1.language_id=t2.language_id"""

    param_dim_currencies_eng = """                                                                                                  
            SELECT                                                                                                                  
            exchange_date, curr_name_eng, currency_source_id, currency_destination_id, exchange_rate, load_rout_timestamp, source_id
            FROM exchange_rates AS t1                                                                                               
            INNER JOIN languages as t2                                                                                              
            ON t1.language_id=t2.language_id
            """
    create_table_dim('dim_currencies', param_dim_currencies)
    create_table_dim('dim_currencies_rus', param_dim_currencies_rus)
    create_table_dim('dim_currencies_eng', param_dim_currencies_eng)


