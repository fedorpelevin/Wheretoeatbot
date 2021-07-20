import json

import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://wheretoeat.ru/winners_2021/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    names = []
    cities = []
    places = []
    first_fifty = soup.find_all('div', class_='image')
    place = 1
    for restaurant in first_fifty:
        if restaurant.parent.parent.parent.get('id') != "special":
            names.append(restaurant.img['title'])
            cities.append(restaurant.find_next(class_='city').text)
            places.append(place)
            place += 1
    rest = soup.find_all('section', class_='rest-of')
    rest_names = rest[0].find_all('span', class_='title')
    rest_names = [name.text for name in rest_names]
    rest_cities = rest[0].find_all('span', class_='city')
    rest_cities = [city.text for city in rest_cities]
    rest_places = rest[0].find_all('span', class_='place')
    rest_places = [place.text for place in rest_places]

    names = names + rest_names
    cities = cities + rest_cities
    places = places + rest_places

    data = {}
    for i in range(len(names)):
        if cities[i] not in data:
            data[cities[i]] = []
        data[cities[i]].append((names[i], places[i]))

    return data


if __name__ == '__main__':
    data = main()
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)
