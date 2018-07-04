import random
import datetime
import time

token = 'TOKEN'

pohvala = ['Восхитительно!', 'Совершенно верно!', 'Изумительно!', 'Вы совершенно правы!', 'Вы знали!', 'Великолепно!',
           'Великолепный ответ!', 'Весьма недурно', 'Вы сама проницательность!', 'Превосходно!', 'Замечательно!',
           'Правильно!', 'Верно!', 'Это правильный ответ!', 'В точку!']
random_message = lambda: random.choice(pohvala)

now = datetime.datetime.now()
cur_hour = now.hour
global greet

if (cur_hour >= 5 and cur_hour < 12):
    timestat = "Доброе утро!"
    greet = timestat
if (cur_hour >= 12 and cur_hour < 18):
    timestat = "Добрый день!"
    greet = timestat
if (cur_hour >= 18 and cur_hour < 24):
    timestat = "Добрый вечер!"
    greet = timestat
if (cur_hour >= 00 and cur_hour < 5):
    timestat = "Доброй ночи!"
    greet = timestat

