CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.source_type (
    source_id INT PRIMARY KEY,
    source VARCHAR(20) COMMENT 'Наименование источника, из которого была получена информация о курсах валют'
    )
    ENGINE=InnoDB;

INSERT INTO core.source_type 
    (source_id, source)
VALUES
    (1, 'ЦБР'),
    (2, 'currencylayer');
