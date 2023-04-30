import telebot
from config import keys, TOKEN
from extension import ConvertionException, APIExeption


bot = telebot.TeleBot(TOKEN) #Подключаемся к @money_converted_bot


@bot.message_handler(commands=['start', 'help']) #При вводе команды /start или /help пользователю выводятся инструкции по применению бота
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите название валюты в формате \n<имя валюты> \ <в какую валюту необходимо перевести>' \
           ' \ <сумма исходной валюты> , \nпример: рубль доллар 100 \nУвидеть список всех доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values']) #При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде
def values(message: telebot.types.Message):
    value = '\n'.join(keys)
    bot.reply_to(message, f"Доступные валюты: \n{value}")


@bot.message_handler(content_types=['text', ]) #Функция проверки и обработки введенных данных пользователем
def echo_test(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Введенных параметров больше или меньше, чем должно быть указано.')

        quote, base, amount = values

        total_base = APIExeption.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Неверно введены данные:\n{e} \nвоспользуйтесь командами:\n/help - для вывода помощи'
                              f'\n/values - для вывода доступных валют')
    except Exception as e:
        bot.reply_to(message, f'Ошибка обработки команды:\n{e} ')
    else:
        text = f'Цена {amount} {keys[quote]}  =  {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True) #Разрешить работу бота при возникновении ошибок











