import telebot
from telebot import types

from service import (
    AbsenceError,
    find_random_restaurant,
    get_restaurant_address,
    find_similar_city_name_in_database,
    count_restaurants
)

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.from_user.id,
        "Привет! Это бот WhereToEatRandom, "
        "который поможет тебе случайным образом выбрать ресторан в твоем городе, "
        "включенный в рейтинг WhereToEat.\n\nНапиши название города, "
        "в котором ты хочешь поесть:")


@bot.message_handler(content_types=['text'])
def check_city(message):
    _city = message.text
    try:
        city = find_similar_city_name_in_database(_city)
        restaurants_count = count_restaurants(city)
    except AbsenceError:
        msg = f'В городе {_city} нет ресторанов из топа WhereToEat. ' \
              f'Рекомендуем вам приготовить что-то восхитительное, не выходя из дома :)'
        bot.send_message(message.from_user.id, msg)
        return

    keyboard = types.InlineKeyboardMarkup()
    key_all = types.InlineKeyboardButton(text=f'Топ-{min(restaurants_count, 15)} ресторанов из города {city}',
                                         callback_data=f'all,{city}')
    keyboard.add(key_all)
    key_random = types.InlineKeyboardButton(text=f'Случайный ресторан из города {city}',
                                            callback_data=f'random,{city}')
    keyboard.add(key_random)
    bot.send_message(message.from_user.id, text='Выберите подходящий вам вариант:', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call_data, city = call.data.split(',')

    if call_data == 'all':
        send_all_restaurants(city, call)

    else:
        send_random_restaurant(city, call, )


def send_all_restaurants(city: str, call):
    restaurants = find_random_restaurant(city, many=True)
    restaurants = restaurants[:min(15, len(restaurants))]  # Количество выводимых ресторанов
    msg = 'Мы нашли вам несколько рестаранов:\n\t' + '\n\t'.join(
        [f'Ресторан "{name}". Место: {place}' for name, place in restaurants])
    bot.send_message(call.from_user.id, msg)


def send_random_restaurant(city: str, call):
    name, place = find_random_restaurant(city)
    msg = f'Вот наше предложение:\n' \
          f'\tНазвание: {name}\n' \
          f'\tМесто в рейтинге: {place}\n'
    bot.send_message(call.from_user.id, msg)


bot.polling()
