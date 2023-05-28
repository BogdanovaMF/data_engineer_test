# test_data_engineer

## Проект представляет собой спроектированную Data Warehouse для хранения информации о курсах конвертации валют RUB, USD, EUR, CNY в СУБД MYSQL.
### Для получения информации о курсах валют были использованы источники: 
- сайт ЦБ РФ https://www.cbr.ru/
- сайт https://currencylayer.com/

*Описание реализованных ETL-процессов*

1. Скрипт `creating_and_populating_tables/create_create_tables.py` - создание таблиц:
- слой Staging - создана таблица `stage_currencies`
- слой Core - созданы таблицы `source_type_3nf`, `languages_3nf`, `exchange_rates_3nf`
2. Скрипт `creating_and_populating_tables/populating_tables.py` заполняет данными таблицы `source_type_3nf` и `languages_3nf`
3. Скрипты `parsing_and_saving_to_db/rubl_every_day.py` и `parsing_and_saving_to_db/ruble_exchange_rate_per_year.py` парсят данные о курсе рубля и конвертации в `USD, EUR, CNY` с сайта ЦБ РФ и сохраняют сырые данные в таблицу `stage_currencies`
4. Скрипты `parsing_and_saving_to_db/usd_every_day.py` и `parsing_and_saving_to_db/usd_exchange_rate_per_year.py` парсят данные о курсе доллара и конвертации в `RUB, EUR, CNY` с сайта https://currencylayer.com/ и сохраняют сырые данные в таблицу `stage_currencies`
5. Скрипт `data_mart/create_and_write_tables` формирует витринные таблицы для анализа `dim_currencies_rus` `dim_currencies_eng`
6. Скрипт `main_run_every_day.py` - запускает процесс обновления таблиц и получения новых данных из источников о курсах валют
#### Чтобы запустить по расписанию, необходимо выполнить команду `cron 0 24 * * * /path_file_main_run_every_day.py`