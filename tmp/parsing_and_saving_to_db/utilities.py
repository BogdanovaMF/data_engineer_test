import requests
from bs4 import BeautifulSoup as bs

from utils import get_logger

logger = get_logger()

def get_values(url, id_valute) -> float:
    """Getting data from url ЦБ РФ
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