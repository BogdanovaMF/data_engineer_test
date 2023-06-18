CREATE SCHEMA IF NOT EXISTS dm;

DROP TABLE IF EXISTS dm.currencies_ru;

CREATE TABLE IF NOT EXISTS dm.currencies_ru (
    exchange_date DATE COMMENT 'Дата обмена валюты',
    language VARCHAR(20) COMMENT 'Конвентируемая валюта на русском языке',
    currency_source_id VARCHAR(10) COMMENT 'Код конвертируемой валюты',
    currency_destination_id VARCHAR(10) COMMENT 'Код валюты, в которую была переведена валюта currency_source_id',
    exchange_rate DECIMAL(10, 4) COMMENT 'Обменный курс',
    load_raw_ts TIMESTAMP COMMENT 'Дата вставки информации о курс обмена в таблицу',
    source VARCHAR(20) COMMENT 'Наименование источника, из которого была получена информация о курсах валют'
    )
    ENGINE=InnoDB;

INSERT INTO dm.currencies_ru
    (exchange_date,
    language,
    currency_source_id,
    currency_destination_id,
    exchange_rate,
    load_raw_ts,
    source
    )
SELECT 
    exchange_date, 
    ru, 
    currency_source_id, 
    currency_destination_id, 
    exchange_rate, 
    load_raw_ts, 
    source
FROM core.exchange_rates AS t1
INNER JOIN core.languages as t2 
ON t1.language_id=t2.language_id
INNER JOIN core.source_type AS t3
ON t1.source_id=t3.source_id;