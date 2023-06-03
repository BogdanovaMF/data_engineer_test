from utils.logger import get_logger
from utils.mysql import mysql_connect

# conn = mysql_connect()
# cursor = conn.cursor()
#
logger = get_logger()


def insert_to_core(table_name_to: str, table_name_from, columns: str) -> None:
    """Inserting data into core from staging
    :param table_name_to: table names to retrieve data
    :param table_name_from: staging table
    :param columns: columns table
    """
    try:
        query = f"""
            INSERT INTO {table_name_to} 
                ({columns})
            SELECT {columns}
            FROM {table_name_from};
            """
        cursor.execute(query)
        conn.commit()
        logger.info(f'Inserting values into a table {table_name_to} completed successfully')
    except Exception as ex:
        logger.error(f'Some error occurred: {ex}')
        conn.rollback()
        raise ex


def update_core(table_name: str, params_query: str):
    """Updating data into core from staging
    :param table_name: table names to retrieve data
    param: params_query: query's parameters
    """
    try:
        queries = f"""
            UPDATE {table_name} {params_query};
        """
        cursor.execute(queries)
        conn.commit()
        logger.info(f'Updating values into a table {table_name} completed successfully')
    except Exception as ex:
        logger.error(f'Some error occurred: {ex}')
        conn.rollback()
        raise ex


if __name__ == '__main__':
    columns = 'exchange_date,source_id, currency_source_id, currency_destination_id, extrange_rate, load_rout_timestamp'
    insert_to_core('stage_currencies', 'exchange_rates', columns)

    params_query1 = "SET language_id=1 WHERE currency_source_id='USD'"
    params_query2 = "SET language_id=2 WHERE currency_source_id='RUB'"
    params_query3 = "SET language_id=4 WHERE currency_source_id='EUR'"
    params_query4 = "SET language_id=3 WHERE currency_source_id='CNY'"
    update_core('exchange_rates', params_query1)
    update_core('exchange_rates', params_query2)
    update_core('exchange_rates', params_query3)
    update_core('exchange_rates', params_query4)

