import config
import requests
from bs4 import BeautifulSoup as our_BS
from aiogram import Bot


bot = Bot(token=config.TOKEN)


def get_messages(message):
    '''
    Функция, с помощью которой анализируем сообщения и отправим данные
    '''
    weather = requests.get(config.WEATHER)
    news = requests.get(config.NEWS)
    html = our_BS(weather.content, 'html.parser')
    html_news = our_BS(news.content, 'html.parser')
    if message.text == 'Погода сегодня':
        text = html.select('#content .wDescription .description')[0].text
        temp = html.select('#blockDays .today-temp')[0].text
        time = html.select('#blockDays .today-time')[0].text
        date = html.select('#bd1 .date')[0].text
        month = html.select('#bd1 .month')[0].text
        t_min = html.select('#bd1 .temperature .min')[0].text
        t_max = html.select('#bd1 .temperature .max')[0].text
        t_day = html.select('#bd1 .day-link')[0].text
        send_message = f"Cегодня {t_day} {date} {month}\n\n{time} {temp}\n\n{t_min}, {t_max}\n\n{text}"

    elif message.text == 'Погода недели':
        send_message = "погода на этой неделе:\n"
        for i in range(1, 7):
            month = html.select(f"#bd{i} .month")[0].text
            t_min = html.select(f"#bd{i} .temperature .min")[0].text
            t_max = html.select(f"#bd{i}  .temperature .max")[0].text
            t_day = html.select(f"#bd{i} .day-link")[0].text
            date = html.select(f"#bd{i} .date")[0].text
            send_message += f"{t_day} {date} {month}\n\n{t_min},{t_max}\n\n\n"
    elif message.text == 'Новости сегодня':
        send_message = "Сегодняшние новости:"
        items = html_news.findAll('div', class_="list-item")
        all_news = []
        for item in items:
            all_news.append(
                item.find('a', class_="list-item__title color-font-hover-only").get_text(strip=True)
            )
        for news in all_news:
            send_message += f"{news}\n\n"
    else:
        send_message = 'Я не знаю что ответить 😢'
    return send_message
