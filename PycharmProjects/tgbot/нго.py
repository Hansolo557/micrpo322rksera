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

bot.polling()
