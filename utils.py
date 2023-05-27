import sys
import logging
import requests
from bs4 import BeautifulSoup as bs


def get_logger():
    """Object logging function"""

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter("%(levelname)s  %(asctime)s: %(message)s"))
    logger.addHandler(handler)

    fh = logging.FileHandler('./file.log')
    fh.setFormatter(logging.Formatter("%(levelname)s  %(asctime)s: %(message)s"))
    logger.addHandler(fh)
    return logger


logger = get_logger()


def get_values(url, id_valute) -> float:
    """Getting data from url
    :param url: link to get data on exchange rates
    :return: rate value
    """
    try:
        response = requests.get(url, timeout=5)
        currency_content = response.text
        soup = bs(currency_content, features="xml")
        value = float(soup.find('Valute', {'ID': id_valute}).find('Value').get_text().replace(',', '.'))

        return value

    except requests.RequestException as ex:
        logger.error(f'Error: {ex}')