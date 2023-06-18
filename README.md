# test_data_engineer

## Проект представляет собой спроектированную Data Warehouse для хранения информации о курсах конвертации валют RUB, USD, EUR, CNY в СУБД MYSQL.
### Для получения информации о курсах валют были использованы источники: 
- сайт ЦБ РФ https://www.cbr.ru/
- сайт https://currencylayer.com/

*Описание реализованных ETL-процессов*

Staging:
1. `staging/ddl/raw_cb_currencies.sql` - создание таблицы `raw.cb_currencies`
2. `staging/ddl/raw_currencylayer_currencies.sql` - создание таблицы `raw.cyrrencylayer_currencies`
3. `staging/crb/crb_client.py` парсит данные о курсе рубля и конвертации в `USD, EUR, CNY` с сайта ЦБ РФ и сохраняет сырые данные в таблицу `raw.cb_currencies`
4. `staging/currencylayer/currencylayer_client.py` парсит данные о курсе рубля и конвертации в `USD, EUR, CNY` с сайта https://currencylayer.com/ и сохраняет сырые данные в таблицу `raw.cyrrencylayer_currencies`

Core: 
1. `core/ddl/core_languages.sql `создает и заполняет данными таблицу `core.languages`
2. `core/ddl/core_source_type.sql `создает и заполняет данными таблицу `source_type`
3. `core/ddl/core_exchange_rates.sql` создает таблицу `core.exchange_rates` и заполняет данными из `raw.cb_currencie` и `raw.cb_currencies`


Data Mart:
1. `dm/ddl/currencies_ru.sql` формирует витринные таблицы для анализа на русском языке `dm.currencies_ru `
2. `dm/ddl/currencies_en.sql` формирует витринные таблицы для анализа на английском языке `dm.currencies_en `


#### Чтобы запустить запись в staging по расписанию, необходимо выполнить команду `cron 0 12 * * * python3 /path_file/data_engineer_test/staging/crb/crb_client.py --table raw.cb_currencies`
#### Чтобы запустить запись в staging по расписанию, необходимо выполнить команду `cron 0 12 * * * python3 /path_file/data_engineer_test/staging/currencylayer/currencylayer_client.py --table raw.cyrrencylayer_currencies`
