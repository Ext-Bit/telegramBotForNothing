from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from datetime import datetime
import os
import sql.query as query
from transcribe_audio.speech_to_text import speech_to_text
import config

answers = ['Да', 'Нет', 'Духи говорят нет', 'Бесспорно', 'Духи говорят да',
            'Спросите позже', 'Возможно', 'Не могу сказать', 'Непонятно',
            'Думаю да', 'Мало шансов', 'Есть сомнения', 'Не сейчас',
            'Точно нет', 'Точно да', 'Очень вероятно', 'Шансы хорошие',
            'Неясно', 'Без сомнений', 'Может быть', 'Сейчас', 'Завтра',
            'Не смей так делать', 'Завтра']


def start_func(message, call=False):
    user_id = message.from_user.id
    username = message.from_user.username
    if call:
        chat_id = message.message.chat.id
    else:
        chat_id = message.chat.id
    print(f'user id: {user_id}  chat id: {chat_id}')
    res = query.select(['username', 'name', 'age', 'step', 'state', 'game_state', 'photo', 'amount_predictions', 'date', 'access_level', 'companion_id', 'request_companion'], 'users', f'id = {user_id}')
    if res == None:
        query.insert('users', ['id', 'username', 'step', 'state', 'game_state', 'date'],
                                            [user_id, username, 1, 0, "None", datetime.now().date()])
        res = query.select(['username', 'name', 'age', 'step', 'state', 'game_state', 'photo', 'amount_predictions', 'date', 'access_level', 'companion_id', 'request_companion'], 'users', f'id = {user_id}')
        bot.send_message(user_id, 'Привет выбери свой возраст из категорий представленных ниже',
                                    reply_markup=gen_markup(button1 = ['0-10', '0-10'],
                                                            button2 = ['11-20', '11-20'],
                                                            button3 = ['21-30', '21-30'],
                                                            button4 = ['31-40', '31-40'],
                                                            button5 = ['41-50', '41-50'],
                                                            button6 = ['51-60', '51-60'],
                                                            button7 = ['61-70', '61-70'],
                                                            button8 = ['71-200', '71-200']))
        return [chat_id, None, res]
    return [chat_id, user_id, res]


def game_results(message, res, chat_id, user_id, var1, var2):
    def check_game_results():
        if game_state in ['30', '31', '32']:
            query.update('users', ['step = 4', 'game_state = "None"'], user_id)
            bot.send_message(chat_id, 'Я победил!!! ЕЕЕЕЕЕ!!! А ты не получишь подарок')
            send_message(message)
        elif game_state in ['03', '13', '23']:
            query.update('users', ['step = 4', 'game_state = "None"'], user_id)
            bot.send_message(chat_id, 'Чтож ты победил, а подарки у нас закончились')
            send_message(message)
    rand = randint(1, 3)
    if rand == 1:
        bot.send_message(chat_id, 'Чтож у нас ничья, давай ещё раз')
    elif rand == 2:
        game_state = res[5][0] + str(int(res[5][1]) + 1)
        query.update('users', [f'game_state = "{game_state}"'], user_id)
        bot.send_message(chat_id, f'Я выбрал {var1} - ты победил')
        check_game_results()
    elif rand == 3:
        game_state = str(int(res[5][0]) + 1) + res[5][1]
        query.update('users', [f'game_state = "{game_state}"'], user_id)
        bot.send_message(chat_id, f'Я выбрал {var2} - я победил')
        check_game_results()


def gen_markup(url=False ,**buttons):
    if len(buttons) > 1:
        arr = []
        n = 1
        if len(buttons) % 2 == 0:
            for i in range(int(len(buttons)/2)):
                arr.append([InlineKeyboardButton(buttons[f'button{n}'][0], callback_data=buttons[f'button{n}'][1]), InlineKeyboardButton(buttons[f'button{n+1}'][0], callback_data=buttons[f'button{n+1}'][1])])
                n += 2
        else:
            for i in range(int(len(buttons)/2)):
                if i == (int(len(buttons)/2)) - 1:
                    arr.append([InlineKeyboardButton(buttons[f'button{n}'][0], callback_data=buttons[f'button{n}'][1])])
                    break
                arr.append([InlineKeyboardButton(buttons[f'button{n}'][0], callback_data=buttons[f'button{n}'][1]), InlineKeyboardButton(buttons[f'button{n+1}'][0], callback_data=buttons[f'button{n+1}'][1])])
                n += 2
        if url:
            arr.append([InlineKeyboardButton('Добавить бота в группу', url='https://t.me/myMegaSuperVeryBigBot?startgroup=true')])
        markup = InlineKeyboardMarkup(arr, row_width=2)

    elif len(buttons) == 1:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(buttons['button1'][0], callback_data=buttons['button1'][1]))
    return markup


API_TOKEN = config.API_TOKEN

bot = TeleBot(API_TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Главное меню')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id, text='', show_alert=False)
    chat_id, user_id, res = start_func(call, True)
    if call.data == 'profile':
        if res[6] == 0:
            bot.send_message(chat_id, f'Username: {res[0]}\nName: {res[1]}\nAge: {res[2]}\nProfile photo: None')
        elif res[6] == 1:
            bot.send_message(chat_id, f'Username: {res[0]}\nName: {res[1]}\nAge: {res[2]}\nProfile photo:')
            file_name = f'photo/image_{user_id}.jpg'
            with open(file_name, 'rb') as image:
                bot.send_photo(chat_id, image)

    elif call.data == '0-10' or call.data == '11-20' or call.data == '21-30' or call.data == '31-40' or call.data == '41-50' or call.data == '51-60' or call.data == '61-70' or call.data == '71-200':
        query.update('users', [f'age = "{call.data}"', 'step = 2'], user_id)
        bot.send_message(chat_id, 'А теперь введите своё имя, только не торопись, мы будем звать тебя так всю жизнь')

    elif call.data == 'game':
        run_game(call)

    elif call.data == 'stop_game':
        query.update('users', ['step = 4', 'game_state = "None"'], user_id)
        bot.send_message(chat_id, 'Игра завершена')
        send_message(call, True)

    elif call.data == 'get_photo':
        bot.send_message(chat_id, 'Отправьте фото...')

    elif call.data == 'dont_get_photo':
        query.update('users', ['step = 4'], user_id)
        bot.send_message(chat_id, 'Регистрация завершена', reply_markup=keyboard)
        bot.send_message(chat_id, 'Теперь ты можешь поиграть со мной, задать мне вопрос или отправить голосовое, чтобы я перевел его в текст',
                                    reply_markup=gen_markup(button1 = ['Показать данные профиля', 'profile'],
                                                            button2 = ['Начать игру', 'game'],
                                                            button3 = ['Секретная кнопка (не трожь)', 'secret_level'],
                                                            button4 = ['Найти собеседника', 'get_companion']))

    elif call.data == 'secret_level':
        if res[8] != datetime.now().date():
            query.update('users', ['amount_predictions = 0', f'date = "{datetime.now().date()}"'], user_id)
            bot.send_message(chat_id, 'Теперь ты можешь получить ответы на все вопрсы')
            bot.send_message(chat_id, 'Просто нажми на кнопку и тебе откроются все тайны мирооздания',
                                        reply_markup=gen_markup(button1 = ['Великая кнопка', 'get_answers']))

        elif res[8] == datetime.now().date() and res[7] >= 3:
            bot.send_message(chat_id, 'Больше предсказания недоступы')
            send_message(call.message, True)

        elif res[8] == datetime.now().date() and res[7] < 3:
            bot.send_message(chat_id, 'Теперь ты можешь получить ответы на все вопрсы')
            bot.send_message(chat_id, 'Просто нажми на кнопку и тебе откроются все тайны мирооздания',
                                        reply_markup=gen_markup(button1 = ['Великая кнопка', 'get_answers']))

    elif call.data == 'get_answers':
        query.update('users', ['step = 999'], user_id)
        bot.send_message(chat_id, 'Введи свой вопрос...')

    elif call.data == 'stop_get_answers':
        query.update('users', ['step = 4'], user_id)
        bot.send_message(chat_id, 'Этот ужас закончен')
        send_message(call.message, True)
    
    elif call.data == 'get_companion':
        if res[10] == 0 and res[11] == 0:
            query.update('users', ['request_companion = 1'], user_id)
            res2 = query.select(['id', 'username'], 'users', f'request_companion = 1 AND id != {user_id}')
            print(res2)
            if not res2:
                bot.send_message(chat_id, 'Ожидайте, идёт поиск',
                                            reply_markup=gen_markup(button1 = ['Остановить поиск', 'stop_request_companion']))
            else:
                query.update('users', [f'companion_id = {res2[0]}', 'request_companion = 2'], user_id)
                query.update('users', [f'companion_id = {user_id}', 'request_companion = 2'], res2[0])
                bot.send_message(chat_id, 'Вы подключены к пользователю '+res2[1],
                                            reply_markup=gen_markup(button1 = ['Отключиться', 'stop_talk']))
                bot.send_message(res2[0], 'Вы подключены к пользователю '+res[0],
                                            reply_markup=gen_markup(button1 = ['Отключиться', 'stop_talk']))
        elif res[11] == 1:
            bot.send_message(chat_id, 'Поиск уже идёт',
                                        reply_markup=gen_markup(button1 = ['Остановить поиск', 'stop_request_companion']))

    elif call.data == 'stop_request_companion':
        query.update('users', ['request_companion = 0', 'companion_id = 0'], user_id)
        bot.send_message(chat_id, 'Поиск остановлен')

    elif call.data == 'stop_talk':
        if res[10] != 0:
            res2 = query.select(['id', 'username'], 'users', f'id = {res[10]}')
            query.update('users', ['request_companion = 0', 'companion_id = 0'], user_id)
            query.update('users', ['request_companion = 0', 'companion_id = 0'], res2[0])
            bot.send_message(chat_id, 'Вы завершили разговор')
            bot.send_message(res2[0], 'Ваш собеседник завершил разговор')
        else:
            bot.send_message(chat_id, 'Разговор уже остановлен')



@bot.message_handler(commands=['start'])
def start_message(message):
    print(message)
    chat_id, user_id, res = start_func(message)
    if message.text == '/start@myMegaSuperVeryBigBot true':
        bot.send_message(chat_id, 'Привет, если ты не зарегистрирован, то перейди в лс с ботом, также там доступы все его функции.\nЗдесь ты можешь задать вопрос боту введя команду: /ask@myMegaSuperVeryBigBot "Ваш вопрос"')
    elif res[4] == 0:
        if res[3] == 1:
            bot.send_message(chat_id, 'Привет выбери свой возраст из категорий представленных ниже',
                                        reply_markup=gen_markup(button1 = ['0-10', '0-10'],
                                                                button2 = ['11-20', '11-20'],
                                                                button3 = ['21-30', '21-30'],
                                                                button4 = ['31-40', '31-40'],
                                                                button5 = ['41-50', '41-50'],
                                                                button6 = ['51-60', '51-60'],
                                                                button7 = ['61-70', '61-70'],
                                                                button8 = ['71-200', '71-200']))
        elif res[3] == 2:
            bot.send_message(chat_id, 'А теперь введите своё имя, только не торопись, мы будем звать тебя так всю жизнь')
        elif res[3] == 3:
            bot.send_message(chat_id, 'Ответьте на вопрос про фото!',
                                        reply_markup=gen_markup(button1 = ['Добавить фото', 'get_photo'],
                                                                button2 = ['Не добавлять фото', 'dont_get_photo']))
        elif res[3] == 4:
            bot.send_message(chat_id, 'Уже начали, иди отсюда',
                                        reply_markup=gen_markup(button1 = ['Показать данные профиля','profile'],
                                                                button2 = ['Начать игру', 'game'],
                                                                button3 = ['Секретная кнопка (не трожь)', 'secret_level'],
                                                                button4 = ['Найти собеседника', 'get_companion']))

    elif res[4] == -1:
        bot.send_message(chat_id, 'Ты в бане уходи')
    else:
        bot.send_message(chat_id, 'Тебе дана безграничная власть, делай что хочешь')


@bot.message_handler(commands=['game'])
def run_game(message):
    chat_id, user_id, res = start_func(message, True)
    if res[3] == 4 and res[4] in [0, 1]:
        query.update('users', ['step = 1000', 'game_state = "00"'], user_id)
        bot.send_message(chat_id, 'Что же давай поиграем в камень-ножницы-бумага, других игр я всё равно не знаю')
        bot.send_message(chat_id, 'Играем до 3-х побед, если ничья то раунд повторяется, кто победил - того приз')
        bot.send_message(chat_id, 'Сейчас ты вводишь слово "камень" или "ножницы" или "бумага", и узнаём кто победил')
        bot.send_message(chat_id, 'Если хочешь остановить игру, или же у нас что-то сломалось нажми сюда',
                                    reply_markup=gen_markup(button1 = ['Стоп', 'stop_game']))
    elif res[3] != 4:
        bot.send_message(chat_id, 'Ах ты хитрец, не не не это так не работает, сначала впиши всю запрашиваемую информацию')
    elif res[4] == -1:
        bot.send_message(chat_id, 'Таким людям как ты игры здесь закрыты, иди подумай над своим поведением')


@bot.message_handler(commands=['ask'])
def send_answer(message):
    chat_id, user_id, res = start_func(message)
    print(message)
    if res[8] != datetime.now().date():
        query.update('users', ['amount_predictions = 0', f'date = "{datetime.now().date()}"'], user_id)
        send_answer(message)
    elif res[8] == datetime.now().date() and res[7] >= 3:
        query.update('users', ['step = 4'], user_id)
        bot.send_message(chat_id, 'Бесплатные вопросы закончились')
    elif res[8] == datetime.now().date() and res[7] < 3:
        if message.text.replace(' ', '')[26:] == '':
            bot.send_message(chat_id, 'Собственно а вопрос где?')
            return
        rand = randint(0, 23)
        bot.send_message(chat_id, answers[rand])
        query.update('users', [f'amount_predictions = {(res[7]+1)}'], user_id)
        if res[7] >= 3:
            bot.send_message(chat_id, 'Бесплатные вопросы закончились')
            send_message(message)


@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id, user_id, res = start_func(message)
    bot.send_message(chat_id, 'Чтобы зарегистрироваться, перейдите в лс к боту.\nНапишите "/ask@myMegaSuperVeryBigBot Ваш вопрос", чтобы бот ответил на вопрос')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    chat_id, user_id, res = start_func(message)
    if res[3] == 3:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = f'photo/image_{user_id}.jpg'
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        query.update('users', ['step = 4', 'photo = 1'], user_id)
        bot.send_message(chat_id, 'Ваше фото загружено. Регистрация завершена', reply_markup=keyboard)
        bot.send_message(chat_id, 'Теперь ты можешь поиграть со мной, задать мне вопрос или отправить голосовое, чтобы я перевел его в текст',
                                    reply_markup=gen_markup(button1 = ['Показать данные профиля', 'profile'],
                                                            button2 = ['Начать игру', 'game'],
                                                            button3 = ['Секретная кнопка (не трожь)', 'secret_level'],
                                                            button4 = ['Найти собеседника', 'get_companion']))

    elif res[4] == 4 and res[11] == 2:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = f'photo_for_chat/image_{user_id}.jpg'
        with open(file_name, 'rb') as image:
            bot.send_photo(res[10], image)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_name = str(message.from_user.id)+'.ogg'
    file_name_conv = str(message.from_user.id)+'.wav'
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(os.getcwd()+'\\transcribe_audio\\'+file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    text = speech_to_text(file_name, file_name_conv)
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def send_message(message, call=False):
    chat_id, user_id, res = start_func(message, call)
    print(message)
    if res[4] == 0:
        if message.text == 'Главное меню' and (res[3] != 0 or res[3] != 1 or res[3] != 2 or res[3] != 3):
            query.update('users', ['step = 4', 'game_state = "None"'], user_id)
            bot.send_message(chat_id, 'Выбери, что тебе хочется',
                                        reply_markup=gen_markup(url=True, button1 = ['Показать данные профиля', 'profile'],
                                                                button2 = ['Начать игру', 'game'],
                                                                button3 = ['Секретная кнопка (не трожь)', 'secret_level'],
                                                                button4 = ['Найти собеседника', 'get_companion']))

        elif res[3] == 1 and user_id != None:
            bot.send_message(chat_id, 'Нет, выбери возраст из категорий ниже',
                                        reply_markup=gen_markup(button1 = ['0-10', '0-10'],
                                                                button2 = ['11-20', '11-20'],
                                                                button3 = ['21-30', '21-30'],
                                                                button4 = ['31-40', '31-40'],
                                                                button5 = ['41-50', '41-50'],
                                                                button6 = ['51-60', '51-60'],
                                                                button7 = ['61-70', '61-70'],
                                                                button8 = ['71-200', '71-200']))

        elif res[3] == 2:
            if len(message.text) < 3 or len(message.text) > 16:
                send_message(chat_id, 'Ник должен быть не короче 3 и не длиннее 16 символов')
            else:
                query.update('users', [f'name = "{message.text}"', 'step = 3'], user_id)
                bot.send_message(chat_id, 'Хочешь ли ты загрузить себе фото профиля?',
                                            reply_markup=gen_markup(button1 = ['Да', 'get_photo'],
                                                                    button2 = ['Нет', 'dont_get_photo']))

        elif res[3] == 3:
            bot.send_message(chat_id, 'Ответьте на вопрос про фото!',
                                        reply_markup=gen_markup(button1 = ['Добавить фото', 'get_photo'],
                                                                button2 = ['Не добавлять фото', 'dont_get_photo']))

        elif res[3] == 4 and res[11] != 2:
            bot.send_message(chat_id, 'Выбери, что тебе хочется',
                                        reply_markup=gen_markup(url=True, button1 = ['Показать данные профиля', 'profile'],
                                                                button2 = ['Начать игру', 'game'],
                                                                button3 = ['Секретная кнопка (не трожь)', 'secret_level'],
                                                                button4 = ['Найти собеседника', 'get_companion']))

        elif res[3] == 4 and res[11] == 2:
            bot.send_message(res[10], message.text)

        elif res[3] == 999:
            if res[8] != datetime.now().date():
                query.update('users', ['amount_predictions = 0', f'date = "{datetime.now().date()}"'], user_id)
                bot.send_message(chat_id, 'Введи свой вопрос...')
            elif res[8] == datetime.now().date() and res[7] >= 3:
                query.update('users', ['step = 4'], user_id)
                bot.send_message(chat_id, 'Всё больше нельзя')
            elif res[8] == datetime.now().date() and res[7] < 3:
                rand = randint(0, 23)
                bot.send_message(chat_id, answers[rand])
                query.update('users', [f'amount_predictions = {(res[7]+1)}'], user_id)
                if res[7] < 2:
                    bot.send_message(chat_id, 'Если хочешь ещё ответов, введи новый вопрос', 
                                                reply_markup=gen_markup(button1 = ['Нехочу', 'stop_get_answers']))
                else:
                    query.update('users', ['step = 4'], user_id)
                    bot.send_message(chat_id, 'Всё больше нельзя')
                    send_message(message)

        elif res[3] == 1000 and res[5] in ['00', '01', '02', '10', '20', '11', '12', '21', '22']:
            if message.text.lower() == 'камень':
                game_results(message, res, chat_id, user_id, 'ножницы', 'бумагу')
            elif message.text.lower() == 'ножницы':
                game_results(message, res, chat_id, user_id, 'бумагу', 'камень')
            elif message.text.lower() == 'бумага':
                game_results(message, res, chat_id, user_id, 'камень', 'ножницы')
            else:
                bot.send_message(chat_id, 'Ты неправильно играешь. Иди прочти правила')

    elif res[4] == -1:
        bot.send_message(chat_id, 'Ты в бане уходи')

    elif res[4] == 1:
        bot.send_message(chat_id, 'Тебе дана безграничная власть, делай что хочешь')



bot.infinity_polling()
