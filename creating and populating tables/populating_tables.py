from utils.mysql import mysql_connect

conn = mysql_connect()
cursor = conn.cursor()

query_insert_languages_3nf = """
        INSERT INTO languages
            (language_id, abbreviation, curr_name_en, curr_name_ger, curr_name_rus, curr_name_chin)
        VALUES 
            (1, 'USD', 'american dollar', 'Amerikanischer Dollar', 'американский доллар', '美元');
        INSERT INTO languages_3nf
            (language_id, abbreviation, curr_name_en, curr_name_ger, curr_name_rus, curr_name_chin)
        VALUES 
            (2, 'RUB', 'russian ruble', 'Russischer Rubel', 'российский рубль', '俄罗斯卢布');
        INSERT INTO languages_3nf
            (language_id, abbreviation, curr_name_en, curr_name_ger, curr_name_rus, curr_name_chin)
        VALUES 
            (3, 'CNY', 'chinese yuan', 'Chinesischer Yuan', 'китайский юань', '中国新年');
        INSERT INTO languages_3nf
            (language_id, abbreviation, curr_name_en, curr_name_ger, curr_name_rus, curr_name_chin)
        VALUES 
            (4, 'EUR', 'euro', 'Euro', 'евро', '欧元');
    """

cursor.execute(query_insert_languages_3nf)
conn.commit()

query_insert_source_type_3nf = """
        INSERT INTO source_type
            (source_id, source)
        VALUES
            (1, 'ЦБР'),
            (2, 'currencylayer')
            ;
    """
cursor.execute(query_insert_source_type_3nf)
conn.commit()