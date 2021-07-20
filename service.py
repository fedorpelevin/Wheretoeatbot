from random import choice
from typing import Union

import requests
from fuzzywuzzy import fuzz

import scrapper

data = scrapper.main()  # база данных
cities = list(data.keys())  # список всех городов из базы данных
least_similarity = 60  # минимальная похожесть введеного пользоателем города на город из базы данных


class AbsenceError(Exception):
    ...


def find_similar_city_name_in_database(city):
    """
    Преобразует название города, которое ввёл пользователь в название города из базы данных
    Возбуждает исключение AbsenceError
    :param city:
    :return:
    """
    res_city = None
    res_similarity = 0

    for _city in cities:
        _similarity = fuzz.ratio(_city, city)
        if _similarity > res_similarity:
            res_city = _city
            res_similarity = _similarity

    if least_similarity > res_similarity:
        raise AbsenceError(f'Не найдено похожих городов. Масимально похожий - {res_city}')

    return res_city


def find_random_restaurant(city: str, many: bool = False) -> Union[tuple, list[tuple]]:
    assert city in cities, 'Упс. ' \
                           'В функцию find_random_restaurant надо передвать город из базы данных'
    if many:
        return data[city]
    return choice(data[city])


def get_restaurant_address(name, city):
    url = f'https://suggest-maps.yandex.ru/suggest-geo?' \
          f'bases=geo%2Cbiz%2Ctransit&' \
          f'client_reqid=1626787275436_379846&' \
          f'lang=ru_RU&' \
          f'll=45.018316%2C53.195063&' \
          f'origin=maps-search-form&' \
          f'outformat=json&' \
          f'part=Ресторан {name}&' \
          f'pos=22&' \
          f'v=9&'

    r = requests.get(url).json()
    res = r['results'][0]['subtitle']['text']
    res = res.removeprefix('Ресторан · ')
    return res

def count_restaurants(city):
    assert city in cities, 'Програмист, ты обосрался. ' \
                           'В функцию get_restaurants_count надо передвать город из базы данных'

    return len(data[city])
