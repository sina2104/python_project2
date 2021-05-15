from aiogram import Bot, Dispatcher, executor, types
import config
from get_messages import get_messages
from sqlighter import SQLighter


bot = Bot(token=config.TOKEN)
d_bot = Dispatcher(bot)
sq = SQLighter('sql_base.db')


@d_bot.message_handler(commands=['start', 'help'])
async def welcome(message):
    '''
    С помошью /start и /help приветствуем пользователя и задаём нужные кнопки для получения данных
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода сегодня")
    item2 = types.KeyboardButton("Погода недели")
    item3 = types.KeyboardButton("Новости сегодня")

    markup.add(item1, item2, item3)

    await bot.send_message(message.chat.id, "Добро пожаловать!\n"
                                            "Я - Sina_moscow_bot,\n"
                                            "бот в котором Сина скажет тебе всё, что москвичу надо!\n"
                                            "Чтобы продолжать, нажмите пожалуйста на /subscribe",
                                            parse_mode='html', reply_markup=markup)
    d_bot.message_handler(content_types=['text'])


@d_bot.message_handler(commands=['subscribe', 'sub'])
async def subscribe(message: types.Message):
    if not sq.subscriber_exists(message.from_user.id):
        # если пользователя нет в базе, добавляем его
        sq.add_subscriber(message.from_user.id)

    else:
        # если он уже есть, то просто обновляем ему статус подписки
        sq.update_subscription(message.from_user.id, True)
    print(sq.get_subscriptions(True))
    await message.answer(
        "Вы успешно подписались на рассылку!")


@d_bot.message_handler(commands=['unsubscribe', 'unsub'])
async def unsubscribe(message: types.Message):
    if not sq.subscriber_exists(message.from_user.id):
        # если пользователя нет в базе, добавляем его с неактивной подпиской
        sq.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        sq.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


@d_bot.message_handler(content_types=['text'])
async def get_message(message):
    send_message = get_messages(message)
    await bot.send_message(message.chat.id, send_message)

if __name__ == '__main__':
    executor.start_polling(d_bot, skip_updates=True)
