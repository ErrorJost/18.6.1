import telebot
from config import TOKEN, keys
from extensions import ConvertionExseption, APIConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    text = 'Привет! Я бот-конвертер валют.\nЧтобы воспользоваться моими возможностями, введите команду через пробел в следующем формате: \n\n<имя переводимой валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\nПример ввода: евро рубль 1\n\nУвидеть все доступные валюты /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'],)
def help(message: telebot.types.Message):
    text = 'Для конвертации валюты введите команду через пробел в следующем формате: \n<имя переводимой валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n\nЗапрос не должен содержать знаки препинания или специальные символы!\n\nПример ввода: евро рубль 1\n\nУвидеть все доступные валюты /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Все доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) < 3:
            raise ConvertionExseption('Слишком мало параметров.Введите запрос еще раз.\nСправка /help')
        elif len(values) > 3:
            raise ConvertionExseption('Введены лишние значения. Введите запрос еще раз.\nСправка /help')

        quote, base, amount = values

        total_base = APIConverter.get_price(quote, base, amount)
    except ConvertionExseption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
         text = f'Цена {amount} {quote} в {base} - {total_base}'
         bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)





