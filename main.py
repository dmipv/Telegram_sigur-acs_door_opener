from aiogram import executor, Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
import yaml


with open(r'config.yml') as file:
    configdata = yaml.load(file, Loader=yaml.FullLoader)
    token_api = configdata['token_api']
    acsserver_ip = configdata['server_ip']
    acsserver_port = configdata['server_port']
    acslogin = configdata['login']
    acspassword = configdata['password']
    users = configdata['users']

bot = Bot(token = token_api)
dp = Dispatcher(bot=bot)



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
   if message.chat.id not in users:
       await bot.send_message(chat_id=message.from_user.id, text='У вас нет доступа. Обратитесь к администратору')
   else:
       await message.answer('Добро пожаловать',
                            reply_markup=get_keyboard())

def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Открыть дверь'))
    return kb

@dp.message_handler(Text(equals='Открыть дверь', ignore_case=True))
async def cmd_start(message: types.Message) -> None:
    if message.chat.id not in users:
        await bot.send_message(chat_id=message.from_user.id, text='У вас нет доступа к этой двери. Обратитесь к администратору')
    else:
        # Импортируем модуль socket в рамках хендлера
        import socket
        # Определяем функцию отправки сообщения. Вставляем параметры подключения в команду
        def send_tcp_message():
            message = f"LOGIN 1.8 {acslogin} {acspassword}\r\nALLOWPASS 9 1447 UNKNOWN\r\n"
            try:
                # Создаем сокет
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Подключаемся по указанному ip адресу и порту сервера СКУД
                s.connect((acsserver_ip, acsserver_port))
                # Отправляем сообщение, при этом кодируем его в битовое представление
                s.send(message.encode('utf-8'))
                # Закрываем сокет
                s.close()
            except Exception as e:
                # Обрабатываем ошибки
                return str(e)

        send_tcp_message()
        # Отправляем сообщение пользователю о том, что у него есть доступ к команде и она отправлена
        await message.answer('Команда отправлена')


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)

