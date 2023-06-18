CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.exchange_rates (
    id SERIAL PRIMARY KEY,
    exchange_date DATE COMMENT 'Дата обмена валюты'
    language_id INT COMMENT 'id языка, который описывает currency_source_id',
    source_id INT COMMENT 'ID источника, из которого была получена информация о курсах валют',
    currency_source_id CHAR(3) COMMENT 'Код конвертируемой валюты',
    currency_destination_id CHAR(3) COMMENT 'Код валюты, в которую была переведена валюта currency_source_id',
    exchange_rate DECIMAL(10, 4) COMMENT 'Обменный курс',
    load_raw_ts TIMESTAMP COMMENT 'Дата вставки информации о курс обмена в таблицу',
    FOREIGN KEY (language_id)  REFERENCES core.languages(language_id),
    FOREIGN KEY (source_id)  REFERENCES core.source_type(source_id)
    )
    ENGINE=InnoDB;


INSERT INTO core.exchange_rates
        (exchange_date, 
        source_id, 
        currency_source_id, 
        currency_destination_id, 
        exchange_rate, 
        load_raw_ts)
    SELECT 
        exchange_date, 
        source_id, 
        currency_source_id, 
        currency_destination_id, 
        exchange_rate, 
        load_raw_ts
    FROM raw.cb_currencies;


INSERT INTO core.exchange_rates
        (exchange_date, 
        source_id, 
        currency_source_id, 
        currency_destination_id, 
        exchange_rate, 
        load_raw_ts)
    SELECT 
        exchange_date, 
        source_id, 
        currency_source_id, 
        currency_destination_id, 
        exchange_rate, 
        load_raw_ts
    FROM raw.cyrrencylayer_currencies;



UPDATE core.exchange_rates SET language_id=1 WHERE currency_source_id='USD';
UPDATE core.exchange_rates SET language_id=2 WHERE currency_source_id='RUB';
UPDATE core.exchange_rates SET language_id=4 WHERE currency_source_id='EUR';
UPDATE core.exchange_rates SET language_id=3 WHERE currency_source_id='CNY';
