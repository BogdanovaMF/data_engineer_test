CREATE SCHEMA IF NOT EXISTS core;

CREATE TABLE IF NOT EXISTS core.languages (
            language_id INT PRIMARY KEY,
            en VARCHAR(50) COMMENT 'Название валюты на английском языке',
            ge VARCHAR(50) COMMENT 'Название валюты на немецком языке',
            ru VARCHAR(50) COMMENT 'Название валюты на русском языке',
            ch VARCHAR(50) COMMENT 'Название валюты на китайском языке'
            )
            ENGINE=InnoDB;

INSERT INTO core.languages
    (language_id, en, ge, ru, ch)
VALUES
    (1, 'american dollar', 'Amerikanischer Dollar', 'американский доллар', '美元');

INSERT INTO core.languages
    (language_id, en, ge, ru, ch)
VALUES
    (2, 'russian ruble', 'Russischer Rubel', 'российский рубль', '俄罗斯卢布');

INSERT INTO core.languages
    (language_id, en, ge, ru, ch)
VALUES
    (3, 'chinese yuan', 'Chinesischer Yuan', 'китайский юань', '中国新年');
    
INSERT INTO core.languages
    (language_id, en, ge, ru, ch)
VALUES
    (4, 'euro', 'Euro', 'евро', '欧元');