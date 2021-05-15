from aiogram import Bot
from bs4 import BeautifulSoup as our_BS
import config
import requests


bot = Bot(token=config.TOKEN)


def get_messages(message):
    '''
    Функция, с помощью которой анализируем сообщения и отправим данные
    '''
    first_day_of_week = 1
    last_day_of_week = 7
    first_element = 0
    weather = requests.get(config.WEATHER)
    news = requests.get(config.NEWS)
    html = our_BS(weather.content, 'html.parser')
    html_news = our_BS(news.content, 'html.parser')
    if message.text == 'Погода сегодня':
        text = html.select('#content .wDescription .description')[first_element].text
        temp = html.select('#blockDays .today-temp')[first_element].text
        time = html.select('#blockDays .today-time')[first_element].text
        date = html.select('#bd1 .date')[first_element].text
        month = html.select('#bd1 .month')[first_element].text
        t_min = html.select('#bd1 .temperature .min')[first_element].text
        t_max = html.select('#bd1 .temperature .max')[first_element].text
        t_day = html.select('#bd1 .day-link')[first_element].text
        send_message = f"Cегодня {t_day} {date} {month}\n\n{time} {temp}\n\n{t_min}, {t_max}\n\n{text}"

    elif message.text == 'Погода недели':
        send_message = "погода на этой неделе:\n"
        for i in range(first_day_of_week, last_day_of_week):
            month = html.select(f"#bd{i} .month")[first_element].text
            t_min = html.select(f"#bd{i} .temperature .min")[first_element].text
            t_max = html.select(f"#bd{i}  .temperature .max")[first_element].text
            t_day = html.select(f"#bd{i} .day-link")[first_element].text
            date = html.select(f"#bd{i} .date")[first_element].text
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
