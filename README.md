Мой телеграм бот помогает людям быстро найти новый хороший(!!!) ресторан/бистро в своем городе, в котором они могут поесть. Поиск случайного ресторана из данного города позволяет людям не думать два часа о том, где им поужинать.

- Файл `bot.py` объединяет всю логику работы бота
- Файл `scrapper.py` парсит данный с сайта `https://wheretoeat.ru/winners_2021/`, забирая оттуда рестораны, города, в которых они расположены и места, которые эти рестораны заняли в топе
- Файл `service.py` содержит функции, помогающие обрабатывать данные: искать максимально похожее на введенное сообщение название города, искать случайный ресторан из данного города и считать количество ресторанов в данном городе

- Для запуска бота надо запустить `bot.py`
