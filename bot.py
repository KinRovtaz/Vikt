# -*- coding: utf-8 -*-
import sqlite3
import datetime
import requests
import telebot
from telebot import apihelper
from telebot import types
import time
import threading
import constans
url = "https://api.telegram.org/bot<constans.token>/"
def get_updates_json(request):
    response = requests.get(request + 'getUpdates')
    return response.json()
def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]
apihelper.proxy = {'https': 'socks5://163.172.152.192:1080'}
bot = telebot.TeleBot(constans.token)
def zerotime():
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    c.execute("UPDATE status SET is_playing =0 WHERE id = 1")
    c.execute("SELECT is_playing FROM status")
    status = c.fetchone()[0]
    print(status)
    conn.commit()
    conn.close()
t = threading.Timer(180.0, zerotime)
t.start()
print ('wait 120 s...')
print ('timestat', constans.greet)
@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    t = threading.Timer(180.0, zerotime)
    t.start()
    c.execute("SELECT is_playing FROM status")
    status = c.fetchone()[0]
    print(status)
    conn.commit()
    conn.close()
    if status == 0:
        conn = sqlite3.connect('vic.db')
        c = conn.cursor()
        c.execute("UPDATE status SET is_playing = 1 WHERE id = 1")
        print(status)
        conn.commit()
        conn.close()
        conn = sqlite3.connect('vic.db')
        c = conn.cursor()
        c.execute("SELECT created_at FROM wons ORDER BY created_at DESC LIMIT 1")
        uw = c.fetchone()[0]
        print('uw', uw)
        today = str(datetime.date.today())
        print('today', today)
        conn.commit()
        conn.close()
        if (uw == today):
            conn = sqlite3.connect('vic.db')
            c = conn.cursor()
            msg = bot.send_message(message.chat.id, 'В настояще время викторина не доступна, сегодня у нас уже есть победитель!')
            c.execute("UPDATE status SET is_playing = 0 WHERE id = 1")
            bot.register_next_step_handler(msg, tostarton)
            conn.commit()
            conn.close()
        else:
            conn = sqlite3.connect('vic.db')
            c = conn.cursor()
            c.execute("SELECT * FROM wons WHERE user_id = " + str(message.from_user.id))
            dont = c.fetchone()
            conn.commit()
            conn.close()
            conn = sqlite3.connect('vic.db')
            c = conn.cursor()
            c.execute("SELECT created_at FROM users WHERE telegram_id = ? ", (str(message.from_user.id),))
            now = c.fetchone()
            c.execute("SELECT name FROM users WHERE telegram_id =" + str(message.from_user.id))
            select = c.fetchone()
            print('now', now)
            print(select)
            conn.commit()
            conn.close()
            today = str(datetime.date.today())
            print(today)
            if select is not None:
                t = threading.Timer(180.0, zerotime)
                t.start()
                bot.send_message(message.chat.id,'О, {select}. Рад снова видеть вас.'.format (select=select[0]))
                if dont is not None:
                    conn = sqlite3.connect('vic.db')
                    c = conn.cursor()
                    msg = bot.send_message(message.chat.id,'Вы уже выиграли свой приз! Пусть и другие попробуют!')
                    c.execute("UPDATE status SET is_playing = 0 WHERE id = 1")
                    bot.register_next_step_handler(msg, tostart)
                    conn.commit()
                    conn.close()
                elif today in now:
                    conn = sqlite3.connect('vic.db')
                    c = conn.cursor()
                    msg = bot.send_message(message.chat.id, 'Cегодня вы уже пытались, приходите завтра.')
                    c.execute("UPDATE status SET is_playing = 0 WHERE id = 1")
                    conn.commit()
                    conn.close()
                    bot.register_next_step_handler(msg, tostarton)
                else:
                     checker(message)
            else:
                bot.send_message(message.chat.id, constans.greet)
                bot.send_message(message.chat.id, 'Чтобы стать победителем, достаточно правильно ответить на 6 вопросов о проекте.')
                sent = bot.send_message(message.chat.id, 'Как вас зовут?')
                bot.register_next_step_handler(sent, hello)
                t = threading.Timer(180.0, zerotime)
                t.start()
    else:
        msg = bot.send_message(message.chat.id,
                               'В настояще время викторина не доступна, кто-то вас опередил, и уже отвечает на вопросы.')
        bot.register_next_step_handler(msg, start)
def hello(message):
    t = threading.Timer(180.0, zerotime)
    t.start()
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    today = str(datetime.date.today())
    bot.send_message(message.chat.id,
             'Привет, {name}. Рад вас видеть.'.format(
                 name=message.text))
    c.execute("INSERT INTO users (name, telegram_id, created_at) VALUES (?, ?, ?) ",
      (message.text, message.from_user.id, today,))
    checker(message)
    conn.commit()
    conn.close()
my_channel_id = "CHANNELID"
def checker(message):
    statuss = ['creator', 'administrator', 'member']
    chri = bot.get_chat_member(chat_id=my_channel_id, user_id=message.from_user.id).status
    t = threading.Timer(180.0, zerotime)
    t.start()
    if chri in statuss:
        bot.send_message(message.chat.id, 'Отлично! Теперь приступим к вопросам. Бот не учитывает регистр и транслитерацию')
        text_ha(message)
    else:
        bot.send_message(message.chat.id, 'Подпишитесь на канал @CHANNELNAME для начала игры')
        sent = bot.send_message(message.chat.id, 'Вы подписались?')
        bot.register_next_step_handler(sent, checker)
def text_ha(message):
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    c.execute("SELECT QE FROM table1")
    questions = c.fetchall()
    sq = bot.send_message(message.chat.id, '{}'.format(questions[0][0]))
    bot.register_next_step_handler(sq, text_handler)
    conn.commit()
    conn.close()
    t = threading.Timer(180.0, zerotime)
    t.start()
@bot.message_handler(func=lambda message: True)
def text_handler(message):
    t = threading.Timer(180.0, zerotime)
    t.start()
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    c.execute("SELECT QE FROM table1")
    questions = c.fetchall()
    c.execute("SELECT OK FROM table1")
    answers = c.fetchall()
    answer = message.text.lower()
    number_of_questions = 5  # len(answers) - 1
    flag = True
    for i in range(number_of_questions):
        if answer in answers[i][0].split(', '):
            flag = False
            bot.reply_to(message, constans.random_message())
            bot.send_message(message.chat.id, '{}'.format(questions[i+1][0]))
            break
    if flag and answer in answers[number_of_questions][0].split(', '):
        flag = False
        bot.reply_to(message, constans.random_message())
        bot.send_message(message.chat.id,
                         'Замечательно! Вы ответили правильно на все вопросы. ')
        bio = bot.send_message(message.chat.id,
                         'Пришлите, пожалуйста, адрес вашего biocoin-кошелька для получения токенов')
        bot.register_next_step_handler(bio, wallet)
    if flag:
        bot.send_message(message.chat.id,
                         'Упс. Нам очень жаль, но вы допустили ошибки. У вас есть возможность попробовать еще раз завтра.')
        tostart(message)
    conn.commit()
    conn.close()
def wallet(message):
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    today = str(datetime.date.today())
    bot.send_message(message.chat.id,
                     'В течение месяца на ваш кошелек: {bi} будут начислены bio'.format(
                         bi=message.text))
    c.execute("SELECT bio FROM wons WHERE user_id =" + str(message.from_user.id))
    base = c.fetchall()
    conn.commit()
    conn.close()
    if base:
        tostart(message)
    else:
        conn = sqlite3.connect('vic.db')
        c = conn.cursor()
        c.execute("INSERT INTO wons (user_id, created_at, bio) VALUES (?, ?, ?) ",
                  (message.from_user.id, today, message.text, ))
        conn.commit()
        conn.close()
    tostart(message)
def tostart(message):
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    msg = bot.send_message(message.chat.id,'Спасибо за игру, удачи!')
    c.execute("UPDATE status SET is_playing = 0 WHERE id = 1")
    conn.commit()
    conn.close()
    conn = sqlite3.connect('vic.db')
    c = conn.cursor()
    c.execute("UPDATE users SET created_at = ? WHERE telegram_id = ?", (str(datetime.date.today()), str(message.from_user.id)))
    conn.commit()
    conn.close()
    bot.register_next_step_handler(msg, start)
def tostarton(message):
    msg = bot.send_message(message.chat.id, 'Викторина будет доступна после 00:00 по Московскому времени!')
    bot.register_next_step_handler(msg, start)
bot.polling(none_stop=True, timeout=300)
