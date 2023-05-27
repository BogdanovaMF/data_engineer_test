from create_connect1 import get_mysql_connection

conn = get_mysql_connection()
cursor = conn.cursor()

stage_currencies_table = """
        CREATE TABLE IF NOT EXISTS stage_currencies (
            pub_date DATE,
            abbreviation1 VARCHAR(10),
            abbreviation2 VARCHAR(10),
            extrange_rate FLOAT,
            source VARCHAR(20)
        );
    """
cursor.execute(stage_currencies_table)
conn.commit()

source_table = """
        CREATE TABLE IF NOT EXISTS source_type_3nf (
            source_id INT PRIMARY KEY,
            source VARCHAR(20)
            )
            ENGINE=InnoDB;
    """

cursor.execute(source_table)
conn.commit()

languages_3nf_table = """
        CREATE TABLE IF NOT EXISTS languages_3nf (
            language_id INT PRIMARY KEY,
            abbreviation VARCHAR(50),
            curr_name_en VARCHAR(50),
            curr_name_ger VARCHAR(50),
            curr_name_rus VARCHAR(50),
            curr_name_chin VARCHAR(50)
            )
            ENGINE=InnoDB;
    """
cursor.execute(languages_3nf_table)
conn.commit()

exchange_rates_3nf_table = """
        CREATE TABLE IF NOT EXISTS exchange_rates_3nf (
            id SERIAL PRIMARY KEY,
            date DATE,
            language_id INT,
            source_id INT,
            abbreviation1 VARCHAR(10),
            abbreviation2 VARCHAR(10),
            exchange_rate FLOAT,
            FOREIGN KEY (language_id)  REFERENCES languages_3nf(language_id),
            FOREIGN KEY (source_id)  REFERENCES source_type_3nf(source_id)
            )
            ENGINE=InnoDB;
    """

cursor.execute(exchange_rates_3nf_table)
conn.commit()

