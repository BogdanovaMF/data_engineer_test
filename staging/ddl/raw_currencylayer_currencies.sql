CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.cyrrencylayer_currencies (
    exchange_date DATE COMMENT 'Дата обмена валюты',
    currency_source_id CHAR(3) COMMENT 'Код конвертируемой валюты',
    currency_destination_id CHAR(3) COMMENT 'Код валюты, в которую была переведена валюта currency_source_id',
    exchange_rate DECIMAL(10, 4) COMMENT 'Обменный курс',
    source_id INT COMMENT 'ID источника, из которого была получена информация о курсах валют', 
    load_raw_ts TIMESTAMP COMMENT 'Дата вставки информации о курс обмена в таблицу',
);