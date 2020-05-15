import telebot
import requests
from bs4 import BeautifulSoup


def send_news():
    url = 'https://mail.ru/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    news = soup.find_all('a', class_='news__list__item__link news__list__item__link_simple')
    all_news = ''
    for new in news:
        all_news += new.get_text() + ' ' + new.get('href') + '\n'
    return all_news


response = requests.get('https://api.telegram.org/bot1188676209:AAEn-FoBoN9LsmqaONEukFk5PcVTF7H27-Y/getUpdates')
data = response.json()

tb = telebot.TeleBot()
list_chat_id = []

for i in data['result']:
    chat_id = (i['message']['from']['id'])
    list_chat_id.append(chat_id)


@tb.message_handler(func=lambda m: True)
def send_msg(message):
    received_news = send_news()
    tb.reply_to(message, received_news)


while True:  # Для постоянной работы
    tb.polling()
