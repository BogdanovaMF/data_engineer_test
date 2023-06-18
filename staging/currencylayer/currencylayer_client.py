import argparse
import os
import time
from datetime import datetime

import currencylayer
import pandas as pd
from dotenv import load_dotenv
from pymysql import Connection

from utils.logger import get_logger
from utils.mysql import insert_data_into_table, mysql_connect


def parse_args():
    """Getting  data from the user from the command line for searching."""
    parser = argparse.ArgumentParser(
        description="Getting the range of dates for currency conversion and the name of "
        "the table in which the data on exchange rates will be entered",
    )
    parser.add_argument("--date_from", help="The beginning of the period for extracting the exchange rate")
    parser.add_argument("--date_to", help="End of period to retrieve exchange rates")
    parser.add_argument("--table_name", required=True, help="Tables name for insert values")
    args = parser.parse_args()
    return vars(args)


class CurrencylayerClient:
    """Class for getting the exchange rate from https://currencylayer.com/."""

    source_code = "currencylayer"
    source_id = 2
    base_currency_code = "USD"

    def __init__(self, conn: Connection | None) -> None:
        self.conn = conn if conn else mysql_connect()
        self.cursor = self.conn.cursor()

    def parse_and_save(
        self,
        currency_codes: list[str],
        table_name: str,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> None:
        """Parsing data from the site and saving to the database
        :param date_from: the beginning of the period for extracting the exchange rate
        :param date_to: end of period to retrieve exchange rates
        :param currency_codes: list with currencies codes
        :param table_name: tables name for insert values.
        """
        if date_from is None and date_to is None:
            date_str = datetime.now().date().today().strftime("%Y-%m-%d")
            currencies = self._request_and_parse(date_str, currency_codes)
            for curr in currencies:
                value = currencies[curr]
                data = (date_str, curr, self.base_currency_code, value, self.source_id, datetime.now())
                insert_data_into_table(table_name, data)

        else:
            daterange = pd.date_range(start=date_from, end=date_to)
            for date in daterange:
                date_str = date.strftime("%Y-%m-%d")
                currencies = self._request_and_parse(date_str, currency_codes)
                for curr in currencies:
                    value = currencies[curr]
                    data = (date, curr, self.base_currency_code, value, self.source_id, datetime.now())
                    insert_data_into_table(table_name, data)
                    time.sleep(1)

    @staticmethod
    def _request_and_parse(date: str, currency_codes: list[str]) -> dict[str, float]:
        """Parsing data from the site
        :param date: exchange rate conversion date
        :param currency_codes: list with currencies code
        :return: dict with currency id and currency rate.
        """
        try:
            exchange_rates = {}
            exchange_rate = currencylayer.Client(access_key=os.getenv("API"))
            data = exchange_rate.historical(date=date, base_currency="USD")
            currencies = data["quotes"]
            for i in currency_codes:
                value = currencies[i]
                exchange_rates[i[3:]] = value
                logger.info(f"From {i[:3]} to {i[3:]} exchange rate = {value}")

            return exchange_rates

        except Exception as ex:
            logger.error(f"Error: {ex}")
            raise ex


if __name__ == "__main__":
    args = parse_args()
    logger = get_logger()
    load_dotenv()
    currency_codes = ["USDRUB", "USDEUR", "USDCNY"]

    curr_layer = CurrencylayerClient(conn=mysql_connect())
    curr_layer.parse_and_save(currency_codes, args["table_name"], args["date_from"], args["date_to"])
