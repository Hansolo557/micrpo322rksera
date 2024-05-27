import random
import telebot
from telebot import types
import webbrowser
import wikipediaapi
from googletrans import Translator

TOKEN = "6326052098:AAEhwesJOT3Y14_9Pu8VfL_iykx6-eAkm-E"
bot = telebot.TeleBot(TOKEN)


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
headers = {'User-Agent': user_agent}
wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)


import requests


def get_book_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            return f'"{data["content"]}" - {data["author"]}'
        else:
            return "Не удалось получить цитату. Попробуйте позже."
    except Exception as e:
        return f"Ошибка: {str(e)}"

@bot.message_handler(commands=['цитата'])
def send_quote(message):
    quote = get_book_quote()
    bot.send_message(message.chat.id, quote)


translator = Translator()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Вики'))
    markup.add(types.KeyboardButton('Чат ЖПТ'))
    bot.send_message(message.chat.id, "Привет! Я бот, который может искать информацию в Википедии или помочь вам вступить в ЖПТ. Выберите нужную функцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == 'вики')
def handle_wikipedia_search(message):
    bot.send_message(message.chat.id, 'Введите слово для поиска в Википедии:')
    bot.register_next_step_handler(message, process_wikipedia_query)

def process_wikipedia_query(message):
    search_query = message.text
    page = wiki_wiki.page(search_query)

    if page.exists():
        bot.send_message(message.chat.id, page.text[:4096])  # Ограничим ответ по длине
    else:
        bot.send_message(message.chat.id, f'По запросу "{search_query}" информация не найдена в Википедии.')

@bot.message_handler(func=lambda message: message.text.lower() == 'чат жпт')
def handle_jpt_chat(message):
    bot.send_message(message.chat.id, 'Присоединяйтесь к Живому Паровозному Трафику (ЖПТ) и общайтесь с единомышленниками! Пройдите по ссылке для вступления: @gigachat_bot')

@bot.message_handler(func=lambda message: message.text.lower() == 'еще поиск')
def handle_search(message):
    bot.send_message(message.chat.id, 'Введите текст для поиска:')
    bot.register_next_step_handler(message, process_search_query)

def process_search_query(message):
    search_query = message.text
    search_url = f'https://www.google.com/search?q={search_query}'
    webbrowser.open(search_url)
    bot.send_message(message.chat.id, f'Выполняется поиск по запросу: {search_query}. Ожидайте, ваш браузер скоро откроется.')

def translate_text(text):
    try:
        translated_text = translator.translate(text, dest='ru').text
        return translated_text
    except Exception as e:
        return f"Ошибка при переводе: {str(e)}"

@bot.message_handler(commands=['translate'])
def translate_message(message):
    bot.send_message(message.chat.id, 'Введите текст для перевода:')
    bot.register_next_step_handler(message, process_translation)

def process_translation(message):
    text = message.text
    translated_text = translate_text(text)
    bot.send_message(message.chat.id, f"Перевод: {translated_text}")


@bot.message_handler(func=lambda message: message.text == '👾')
def handle_games(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Угадай число')
    button2 = types.KeyboardButton('Викторина')
    button3 = types.KeyboardButton('↩️ Назад в меню')

    markup.row(button1)
    markup.row(button2)
    markup.row(button3)

    bot.send_message(message.chat.id, 'Добро пожаловать в раздел игр! Выберите игру:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Угадай число')
def handle_guess_number_game(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в игру "Угадай число"!\nЯ загадал число от 1 до 100. Попробуйте угадать его!')

    # сан табам
    secret_number = random.randint(1, 100)

    # Определяем функцию обработки ответов пользователя
    def check_guess(msg, secret):
        try:
            guess = int(msg.text)
            if guess == secret:
                bot.send_message(msg.chat.id, f'Поздравляю! Вы угадали число {secret}!')
            elif guess < secret:
                bot.send_message(msg.chat.id, 'Нет, загаданное число больше.')
                # После каждой попытки угадать число, вызываем функцию для новой попытки
                bot.register_next_step_handler(msg, lambda m: check_guess(m, secret))
            else:
                bot.send_message(msg.chat.id, 'Нет, загаданное число меньше.')
                # После каждой попытки угадать число, вызываем функцию для новой попытки
                bot.register_next_step_handler(msg, lambda m: check_guess(m, secret))
        except ValueError:
            bot.send_message(msg.chat.id, 'Пожалуйста, введите целое число.')

    # Регистрируем функцию обработки ответов пользователя для первой попытки
    bot.register_next_step_handler(message, lambda m: check_guess(m, secret_number))

@bot.message_handler(func=lambda message: message.text == 'Викторина')
def handle_quiz_game(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в игру "Викторина"!')

    questions_answers = {
        'Сколько планет в солнечной системе?': '8',
        'Какой химический элемент находится на первом месте в таблице химических элементов?': 'Водород',
        'Как называется столица Франции?': 'Париж',
        'Какой самый высокий горный хребет на планете Земля?': 'Гималаи',
        'Как называется космический аппарат, запущенный СССР в 1957 году?': 'Спутник'
    }

    def start_quiz(msg, qa):
        question = random.choice(list(qa.keys()))
        bot.send_message(msg.chat.id, question)
        bot.register_next_step_handler(msg, lambda m: check_answer(m, qa, question))

    def check_answer(msg, qa, question):
        user_answer = msg.text.strip()
        correct_answer = qa[question]
        if user_answer.lower() == correct_answer.lower():
            bot.send_message(msg.chat.id, 'Правильно!')
            # После правильного ответа отправляем следующий вопрос
            del qa[question]
            if qa:
                start_quiz(msg, qa)
            else:
                bot.send_message(msg.chat.id, 'Поздравляю! Викторина завершена.')
        else:
            bot.send_message(msg.chat.id, f'Неправильно! Правильный ответ: {correct_answer}')
            # После неправильного ответа отправляем следующий вопрос
            start_quiz(msg, qa)

    start_quiz(message, questions_answers)

# Ваш остальной код...


@bot.message_handler(func=lambda message: message.text.lower() == 'вики')
def handle_wikipedia_search(message):
    bot.send_message(message.chat.id, 'Введите слово для поиска в Википедии:')
    bot.register_next_step_handler(message, process_wikipedia_query)

def process_wikipedia_query(message):
    search_query = message.text
    page_py = wiki_wiki.page(search_query)

    if page_py.exists():
        # Если страница существует, отправляем пользователю ее краткое описание
        bot.send_message(message.chat.id, page_py.text[:4096])  # Ограничим ответ по длине
    else:
        bot.send_message(message.chat.id, f'По запросу "{search_query}" информация не найдена в Википедии.')



# Добавляем логику для кнопки "Поиск"
@bot.message_handler(func=lambda message: message.text.lower() == 'еще поиск')
def handle_search(message):
    # Здесь можно добавить дополнительные действия перед отправкой запроса в браузер
    bot.send_message(message.chat.id, 'Введите текст для поиска:')
    bot.register_next_step_handler(message, process_search_query)

def process_search_query(message):
    search_query = message.text
    search_url = f'https://www.google.com/search?q={search_query}'
    webbrowser.open(search_url)
    bot.send_message(message.chat.id, f'Выполняется поиск по запросу: {search_query}. Ожидайте, ваш браузер скоро откроется.')

# Ваш текущий код...

answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.', 'Мой разработчик не говорил, что отвечать в такой ситуации... >_<']


# Добавим ссылки на фильмы в словарь movie_links
movie_links = {
    'Фильм #1': 'https://zetflixhdcm17.kinos.cam/serial/23112872~%D0%91%D0%B5%D1%81%D0%BF%D0%BE%D1%89%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9',
    'Фильм #2': 'https://zetflixhdcm17.kinos.cam/film/23116072~%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD+%D0%9C%D0%B8%D0%BB%D0%BB%D0%B5%D1%80',
    'Фильм #3': 'https://zetflixhdcm17.kinos.cam/film/23117476~%D0%92%D0%B7%D1%80%D0%BE%D1%81%D0%BB%D1%8B%D0%B5+%D0%BD%D0%B5+%D0%B7%D0%BD%D0%B0%D1%8E%D1%82',
    'Фильм #4': 'https://zetflixhdcm17.kinos.cam/film/23115136~%D0%A1%D0%BF%D1%80%D0%B8%D0%BD%D0%B3-%D0%9B%D1%8D%D0%B9%D0%BA%D1%81',
}

# Определение бота и другие глобальные переменные
# ...

# Обработка выбора фильма
@bot.message_handler(func=lambda message: message.text.startswith('Фильм #'))
def handle_movie_choice(message):
    # Добавьте логику для обработки выбранного фильма
    movie_number = message.text.split('#')[-1].strip()
    movie_link = movie_links.get(f'Фильм #{movie_number}', 'Ссылка на фильм не найдена.')

    if movie_link != 'Ссылка на фильм не найдена.':
        bot.send_message(message.from_user.id, f'Ссылка на просмотр Фильма #{movie_number}: {movie_link}')
    else:
        bot.send_message(message.chat.id, 'Извините, произошла ошибка при получении ссылки на фильм.')

# Ваш текущий код...

photo_links = {
    '🔹 Товар #1': 'https://avatars.dzeninfra.ru/get-zen_doc/1889318/pub_5f872f3a17c9884cd30be8c0_5f872faeaa68813be1771c8e/scale_1200',
    '🔹 Товар #2': 'https://i.ytimg.com/vi/gfvqRBQk7vw/maxresdefault_live.jpg',
    '🔹 Товар #3': 'https://cdn2.mygazeta.com/i/2017/08/maxresdefault1.jpg',
    '🔹 Товар #4': 'https://amazingsoftbd.com/wp-content/uploads/2018/10/htmlcss.jpg',
}

product_prices = {
    '🔹 Товар #1': 45000.000,
    '🔹 Товар #2': 42000.000,
    '🔹 Товар #3': 38000.000,
    '🔹 Товар #4': 55000.000,
}

cart_items = set()

user_carts = {}

def create_payment(total_price):
    return '4400 4300 4444 4444'

def process_payment(payment_id):
    return True

course_links = {
    '🔹 Курс Python': 'https://link-to-python-course',
    '🔹 Курс JavaScript': 'https://link-to-javascript-course',
    '🔹 Курс HTML/CSS': 'https://link-to-html-css-course',
}

course_prices = {
    '🔹 Курс Python': 10000.000,
    '🔹 Курс JavaScript': 12000.000,
    '🔹 Курс HTML/CSS': 8000.000,
}

qr_code_url = 'http://tvoy-bor.ru/image/news/city/2021/10/kod.jpg'
botfather_url = 'https://t.me/botfather'



@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    if user_id not in user_carts:
        user_carts[user_id] = set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Товары')
    button2 = types.KeyboardButton('🎓 Курсы')
    button3 = types.KeyboardButton('⚙️ Настройки')
    button4 = types.KeyboardButton('📄 Справка')
    button5 = types.KeyboardButton('🛒 Корзина')
    button6 = types.KeyboardButton('👾')
    button7 = types.KeyboardButton('🎬 Кинорум')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5, button7)
    markup.row(button6)

    cart_content = ', '.join(user_carts[user_id]) if user_carts[user_id] else 'пуста'
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nУ меня ты сможешь купить некоторые товары, записаться на курсы или поиграть в игры!'
                                      f'\n\nТвоя корзина: {cart_content}', reply_markup=markup)

@bot.message_handler(content_types='photo')
def get_photo(message):
    bot.send_message(message.chat.id, 'У меня нет возможности просматривать фото :(')

@bot.message_handler(commands=['photo1', 'photo2', 'photo3', 'photo4'])
def send_product_photos(message):
    command = message.text[1:]
    product_name = f'🔹 Товар #{command[-1]}'
    send_product_photo(message, product_name)

@bot.message_handler()
def info(message):
    if message.text == '🛍 Товары':
        goodsChapter(message)
    elif message.text == '🎓 Курсы':
        coursesChapter(message)
    elif message.text == '⚙️ Настройки':
        settingsChapter(message)
    elif message.text == '📄 Справка':
        infoChapter(message)
    elif message.text == '👾':
        handle_games(message)
    elif message.text.startswith('🔹 Товар #'):
        send_product_photo(message, message.text)
    elif message.text == '💳 Купить':
        buy_products(message)
    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        welcome(message)
    elif message.text == '🔹 Курс Python' or message.text == '🔹 Курс JavaScript' or message.text == '🔹 Курс HTML/CSS':
        send_course_info(message)
    elif message.text == '💳 Купить курс':
        buy_course(message)
    elif message.text == '🛒 Корзина':
        show_cart(message)
    elif message.text.lower() in ["🎬 кинорум", "🎬кинорум", "кинорум"]:
        handle_kinoroom_menu(message)
    else:
        bot.send_message(message.chat.id, answers[random.randint(0, 3)])

def goodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Товар #1')
    button2 = types.KeyboardButton('🔹 Товар #2')
    button3 = types.KeyboardButton('🔹 Товар #3')
    button4 = types.KeyboardButton('🔹 Товар #4')
    button5 = types.KeyboardButton('💳 Купить')
    button6 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5, button6)
    bot.send_message(message.chat.id, 'Вот все товары, которые сейчас находятся в продаже:', reply_markup=markup)

def coursesChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Курс Python')
    button2 = types.KeyboardButton('🔹 Курс JavaScript')
    button3 = types.KeyboardButton('🔹 Курс HTML/CSS')
    button4 = types.KeyboardButton('💳 Купить курс')
    button5 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    bot.send_message(message.chat.id, 'Вот все курсы, на которые вы можете записаться:', reply_markup=markup)

def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('⚙️ Настройки #1')
    button2 = types.KeyboardButton('⚙️ Настройки #2')
    button3 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3)
    bot.send_message(message.chat.id, 'Раздел настроек.\nВыбери один из вариантов:', reply_markup=markup)

def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику')
    button2 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, f'Раздел справки.\nЗдесь ты можешь написать моему разработчику.\nДля этого перейди по ссылке: {botfather_url}', reply_markup=markup)



def send_product_photo(message, product_name):
    if product_name in photo_links:
        if product_name in cart_items:
            photo_url = photo_links[product_name]
            bot.send_photo(message.chat.id, photo_url, caption=f'Описание {product_name}\nТовар уже в корзине.')
        else:
            photo_url = photo_links[product_name]
            price = product_prices.get(product_name, 0.00)
            bot.send_photo(message.chat.id, photo_url, caption=f'Описание {product_name}\nЦена: ₸{price}\nДобавлено в корзину.')
            cart_items.add(product_name)
    else:
        bot.send_message(message.chat.id, 'Фото товара не найдено.')

def buy_products(message):
    user_id = message.from_user.id
    if user_id not in user_carts:
        user_carts[user_id] = set()

    if cart_items:
        total_price = sum(product_prices.get(item, 0.00) for item in cart_items)
        payment_id = create_payment(total_price)

        if process_payment(payment_id):
            user_carts[user_id].update(cart_items)
            cart_items.clear()

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='✅ Я оплатил', callback_data='paid'))
            markup.add(types.InlineKeyboardButton(text='✖️ Отменить', callback_data='cancel'))

            bot.send_photo(message.chat.id, qr_code_url,
                           caption=f'Сканируйте QR-код для оплаты\nKASPI GOLD\n\nФорма оплаты: KASPI\n\n1⃣ Отправить счет ниже👇\n\n💳 4400 4300 4444 4444',
                           reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ошибка при обработке платежа. Пожалуйста, попробуйте еще раз.')
    else:
        bot.send_message(message.chat.id, 'Ваша корзина пуста. Выберите товары для покупки.')

def send_course_info(message):
    course_name = message.text
    if course_name in course_links:
        if course_name in cart_items:
            course_url = course_links[course_name]
            bot.send_message(message.chat.id, f'Описание {course_name}\nКурс уже в корзине.\n{course_url}')
        else:
            course_url = course_links[course_name]
            price = course_prices.get(course_name, 0.00)
            bot.send_message(message.chat.id, f'Описание {course_name}\nЦена: ₸{price}\nДобавлено в корзину.\n{course_url}')
            cart_items.add(course_name)
    else:
        bot.send_message(message.chat.id, 'Информация о курсе не найдена.')

def buy_course(message):
    user_id = message.from_user.id
    if user_id not in user_carts:
        user_carts[user_id] = set()

    if cart_items:
        total_price = sum(course_prices.get(item, 0.00) for item in cart_items)
        payment_id = create_payment(total_price)

        if process_payment(payment_id):
            user_carts[user_id].update(cart_items)
            cart_items.clear()

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='✅ Я оплатил', callback_data='paid'))
            markup.add(types.InlineKeyboardButton(text='✖️ Отменить', callback_data='cancel'))

            bot.send_photo(message.chat.id, qr_code_url,
                           caption=f'Сканируйте QR-код для оплаты\nKASPI GOLD\n\nФорма оплаты: KASPI\n\n1⃣ Отправить счет ниже👇\n\n💳 4400 4300 4444 4444',
                           reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ошибка при обработке платежа. Пожалуйста, попробуйте еще раз.')
    else:
        bot.send_message(message.chat.id, 'Ваша корзина пуста. Выберите курсы для покупки.')

def show_cart(message):
    user_id = message.from_user.id
def show_cart(message):
    user_id = message.from_user.id
    cart_content = ', '.join(user_carts[user_id]) if user_carts[user_id] else 'пуста'
    bot.send_message(message.chat.id, f'Твоя корзина: {cart_content}')

def handle_kinoroom_menu(message):
    # Добавьте здесь логику обработки команд для кинорума
    bot.send_message(message.chat.id, 'Кинорум находится в разработке. Приходите позже!')



@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'paid':
        bot.send_message(call.message.chat.id, 'Оплата прошла успешно. Спасибо за покупку!')
    elif call.data == 'cancel':
        bot.send_message(call.message.chat.id, 'Оплата отменена. Попробуйте выбрать товары заново.')


# Ваш текущий код...

# Добавим ссылки на фильмы в словарь movie_links
movie_links = {
    'Фильм #1': 'https://zetflixhdcm17.kinos.cam/serial/23112872~%D0%91%D0%B5%D1%81%D0%BF%D0%BE%D1%89%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9',
    'Фильм #2': 'https://zetflixhdcm17.kinos.cam/film/23116072~%D0%9A%D0%B0%D0%BF%D0%B8%D1%82%D0%B0%D0%BD+%D0%9C%D0%B8%D0%BB%D0%BB%D0%B5%D1%80',
    'Фильм #3': 'https://zetflixhdcm17.kinos.cam/film/23117476~%D0%92%D0%B7%D1%80%D0%BE%D1%81%D0%BB%D1%8B%D0%B5+%D0%BD%D0%B5+%D0%B7%D0%BD%D0%B0%D1%8E%D1%82',
    'Фильм #4': 'https://zetflixhdcm17.kinos.cam/film/23115136~%D0%A1%D0%BF%D1%80%D0%B8%D0%BD%D0%B3-%D0%9B%D1%8D%D0%B9%D0%BA%D1%81',
}

# Добавим логику для обработки команды "Кинорум"
def handle_kinoroom_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Фильм #1')
    button2 = types.KeyboardButton('Фильм #2')
    button3 = types.KeyboardButton('Фильм #3')
    button4 = types.KeyboardButton('Фильм #4')
    button5 = types.KeyboardButton('↩️ Назад в меню')

    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)

    bot.send_message(message.chat.id, 'Добро пожаловать в Кинорум! Выберите фильм для просмотра:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.startswith('Фильм #'))
def handle_movie_choice(message):

    movie_number = message.text.split('#')[-1].strip()
    movie_link = movie_links.get(f'Фильм #{movie_number}', 'Ссылка на фильм не найдена.')

    if movie_link != 'Ссылка на фильм не найдена.':
        bot.send_message(message.from_user.id, f'Ссылка на просмотр Фильма #{movie_number}: {movie_link}')
    else:
        bot.send_message(message.chat.id, 'Извините, произошла ошибка при получении ссылки на фильм.')




if __name__ == '__main__':
    bot.polling(none_stop=True)