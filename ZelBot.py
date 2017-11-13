# -*- coding: utf-8 -*-
import config
import telebot
import func
import qwests

bot = telebot.TeleBot(config.token)

db = func.open_file('db.csv')

#  Старт квеста
@bot.message_handler(commands = ['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start', '/qwest', '/loc')
    user_markup.row('/help', '/again')
    Uid = message.chat.id
    ent = func.ent_user(Uid, db)
    func.save_file(db)
    if ent == False:
        bot.send_message(message.chat.id, qwests.welcome1, reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, qwests.welcome2, reply_markup=user_markup)


#  Запрос текущего квеста
@bot.message_handler(commands = ['qwest'])
def current_qwest(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start', '/qwest', '/loc')
    user_markup.row('/help', '/again')
    Uid = message.chat.id
    CQ = func.my_qwest(Uid, db)
    if CQ == 1:
        bot.send_message(message.chat.id, qwests.qwest1, reply_markup=user_markup)
    if CQ == 2:
        bot.send_message(message.chat.id, qwests.qwest2, reply_markup=user_markup)
    if CQ == 3:
        bot.send_message(message.chat.id, qwests.qwest3, reply_markup=user_markup)


#  Отправка геолокации
@bot.message_handler(commands = ['loc'])
def geoloc(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Отправь мне свое местоположение!", reply_markup=keyboard)

#  Обработка местоположения
@bot.message_handler(content_types = ['location'])
def get_geoloc(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('/start', '/qwest', '/loc')
    user_markup.row('/help', '/again')
    loc = message.location
    print(loc)
    Uid = message.chat.id
    my_loc = func.norm_loc(loc)
    CQ = func.my_qwest(Uid, db)
    rez = func.in_right_place(Uid, db, my_loc, CQ)
    if rez == True:
        func.next_qwest(Uid, db)
        bot.send_message(message.chat.id, 'Поздравляем! Чтобы посмотреть следующий квест, нажмите /qwest', reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, 'Вы не угадали, подумайте еще! Чтобы заново посмотреть задание, нажмите /qwest', reply_markup=user_markup)
    user_markup = telebot.types.ReplyKeyboardMarkup(True)


if __name__ == '__main__':
    bot.polling(none_stop=True)
