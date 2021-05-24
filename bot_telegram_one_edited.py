import telebot
import bot_telegram_token
import requests
from telebot import types
from bs4 import BeautifulSoup as BS

r = requests.get('https://yandex.ru/news/quotes/2002.html')

html = BS(r.content, 'html.parser')

bot = telebot.TeleBot(bot_telegram_token.BOT_TOKEN)



for el in html.select(".quote__data"):
    course = el.select('.quote__day .quote__value')[0].text
    up = el.select('.quote__day .quote__change')[0].text


r2 = requests.get('https://yandex.ru/news/quotes/23.html')

html2 = BS(r2.content, 'html.parser')

for el in html2.select('.quote__data'):
    course2 = el.select('.quote__day .quote__value')[0].text
    up2 = el.select('.quote__day .quote__change')[0].text


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот Doggo')

    bot.send_message(message.chat.id, 'ты можешь ввести команды "доллар" "евро" и'
                                      ' тебе выведется вся текущая информация')

    


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.type == 'private':
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id, 'привет, чё как?')
        elif message.text.lower() == 'пока':
            bot.send_message(message.chat.id, 'всего наилучшего')
        elif message.text.lower() == 'доллар':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item_first = types.InlineKeyboardButton("Изменение", callback_data='change')
            item_second = types.InlineKeyboardButton("Курс", callback_data='value')

            markup.add(item_first, item_second)

        elif message.text.lower() == 'евро':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item_third = types.InlineKeyboardButton("Изменение", callback_data='change_eu')
            item_fourth = types.InlineKeyboardButton("Курс", callback_data='value_eu')

            markup.add(item_third, item_fourth)

        else:
            bot.send_message(message.chat.id, 'ты спрашиваешь меня о том, чего я не знаю')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'change':
                bot.send_message(call.message.chat.id, course)
            elif call.data == 'value':
                bot.send_message(call.message.chat.id, up)
            elif call.data == 'change_eu':
                bot.send_message(call.message.chat.id, course2)
            elif call.data == 'value_eu':
                bot.send_message(call.message.chat.id, up2)



    except Exception as e:
        print(repr(e))


bot.polling()