import config
import requests
from bs4 import BeautifulSoup as our_BS
from telebot import types
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter


bot = Bot(token=config.TOKEN)
d_bot = Dispatcher(bot)
sq = SQLighter('sql_base.db')


@d_bot.message_handler(commands=['start', 'help'])
async def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Погода сегодня")
    item2 = types.KeyboardButton("Погода недели")
    item3 = types.KeyboardButton("Новости сегодня")

    markup.add(item1, item2, item3)

    await bot.send_message(message.chat.id,
                                          "Добро пожаловать!\n"
                                          "Я - Sina_moscow_bot,\n"
                                          "бот в котором Сина скажет тебе всё, что москвичу надо!\n"
                                          "Чтобы продолжать, нажмите пожалуйста на /subscribe".format(
                                           message.from_user, bot.get_me()),
                                          parse_mode='html', reply_markup=markup)
    d_bot.message_handler(content_types=['text'])


@d_bot.message_handler(commands=['subscribe', 'sub'])
async def subscribe(message: types.Message):
    if (not sq.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        sq.add_subscriber(message.from_user.id)

    else:
        # если он уже есть, то просто обновляем ему статус подписки
        sq.update_subscription(message.from_user.id, True)
    print(sq.get_subscriptions(True))
    await message.answer(
        "Вы успешно подписались на рассылку!")


@d_bot.message_handler(commands=['unsubscribe', 'unsub'])
async def unsubscribe(message: types.Message):
    if (not sq.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        sq.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        sq.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


@d_bot.message_handler(content_types=['text'])
async def get_message(message):
    weather = requests.get(config.WEATHER)
    news = requests.get(config.NEWS)
    html = our_BS(weather.content, 'html.parser')
    html_news = our_BS(news.content, 'html.parser')
    if message.chat.type == 'private':
        if message.text == 'Погода сегодня':
            text = html.select('#content .wDescription .description')[0].text
            temp = html.select('#blockDays .today-temp')[0].text
            time = html.select('#blockDays .today-time')[0].text
            date = html.select('#bd1 .date')[0].text
            month = html.select('#bd1 .month')[0].text
            t_min = html.select('#bd1 .temperature .min')[0].text
            t_max = html.select('#bd1 .temperature .max')[0].text
            t_day = html.select('#bd1 .day-link')[0].text
            await bot.send_message(message.chat.id, f"Cегодня {t_day} {date} {month}\n\n{time} {temp}\n\n"
                                              f"{t_min}, {t_max}\n\n{text}")


        elif message.text == 'Погода недели':
            await bot.send_message(message.chat.id, f"погода на этой неделе:\n")
            for i in range(1, 7):
                month = html.select(f"#bd{i} .month")[0].text
                t_min = html.select(f"#bd{i} .temperature .min")[0].text
                t_max = html.select(f"#bd{i}  .temperature .max")[0].text
                t_day = html.select(f"#bd{i} .day-link")[0].text
                date = html.select(f"#bd{i} .date")[0].text
                await bot.send_message(message.chat.id, f"{t_day} {date} {month}\n\n{t_min},{t_max}")
        elif message.text == 'Новости сегодня':
            items = html_news.findAll('div', class_="list-item")
            all_news = []
            for item in items:
                all_news.append(
                    item.find('a', class_="list-item__title color-font-hover-only").get_text(strip=True)
                )
            for news in all_news:
                await bot.send_message(message.chat.id, news)
        else:
            await bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


if __name__ == '__main__':
    executor.start_polling(d_bot, skip_updates=True)

