from utils.mysql import mysql_connect

conn = mysql_connect()
cursor = conn.cursor()

stage_currencies_table = """
        CREATE TABLE IF NOT EXISTS stage_currencies (
            exchange_date DATE,
            currency_source_id CHAR(3),
            currency_destination_id CHAR(3),
            extrange_rate DECIMAL(10, 4),
            source VARCHAR(20),
            load_rout_timestamp TIMESTAMP
        );
    """
cursor.execute(stage_currencies_table)
conn.commit()
#
# source_table = """
#         CREATE TABLE IF NOT EXISTS source_type (
#             source_id INT PRIMARY KEY,
#             source VARCHAR(20)
#             )
#             ENGINE=InnoDB;
#     """
#
# cursor.execute(source_table)
# conn.commit()
#
# languages_3nf_table = """
#         CREATE TABLE IF NOT EXISTS languages (
#             language_id INT PRIMARY KEY,
#             currency_id VARCHAR(20),
#             curr_name_en VARCHAR(50),
#             curr_name_ger VARCHAR(50),
#             curr_name_rus VARCHAR(50),
#             curr_name_chin VARCHAR(50)
#             )
#             ENGINE=InnoDB;
#     """
# cursor.execute(languages_3nf_table)
# conn.commit()
#
# exchange_rates_table = """
#         CREATE TABLE IF NOT EXISTS exchange_rates (
#             id SERIAL PRIMARY KEY,
#             exchange_date DATE,
#             language_id INT,
#             source_id INT,
#             currency_source_id VARCHAR(10),
#             currency_destination_id VARCHAR(10),
#             exchange_rate FLOAT,
#             load_rout_timestamp TIMESTAMP,
#             FOREIGN KEY (language_id)  REFERENCES languages(language_id),
#             FOREIGN KEY (source_id)  REFERENCES source_type(source_id)
#             )
#             ENGINE=InnoDB;
#     """
#
# cursor.execute(exchange_rates_table)
# conn.commit()

