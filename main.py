import os
import time

import requests
import telegram
from dotenv import load_dotenv


def send_telegram_message(devman_lesson, bot, chat_id):
    accept_work = devman_lesson['new_attempts'][0]['is_negative']
    lesson_title = devman_lesson['new_attempts'][0]['lesson_title']
    lesson_url = devman_lesson['new_attempts'][0]['lesson_url']
    full_lesson_url = f'https://dvmn.org{lesson_url}'
    if accept_work:
        message = f'У вас проверили работу "{lesson_title}"' \
                  '\n\nК сожеление, в работе нашлись ошибки.' \
                  f'\n{full_lesson_url}'
        bot.send_message(text=message, chat_id=chat_id)
        return
    message = f'У вас проверили работу "{lesson_title}"' \
              '\n\nПреподователю все понравилось можно приступить к' \
              'следующему уроку.'
    bot.send_message(text=message, chat_id=chat_id)


def get_result_cheking_works(devman_token, telegram_bot, telegram_chat_id,
                             timestamp=None):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': devman_token}
    payload = {'timestamp': timestamp}
    while True:
        response = requests.get(url, headers=headers, params=payload,
                                timeout=60)
        lesson = response.json()
        status = lesson['status']
        if status == 'timout':
            request_timestamp = lesson['timestamp_to_request']
            payload = {'timestamp': request_timestamp}
        elif status == 'found':
            payload = {'timestamp': timestamp}
            send_telegram_message(lesson, telegram_bot, telegram_chat_id)

if __name__ == '__main__':
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    telegram_bot = telegram.Bot(token=telegram_token)
    while True:
        try:
            get_result_cheking_works(devman_token, telegram_bot,
                                     telegram_chat_id)
        except requests.exceptions.ReadTimeout:
            time.sleep(10)
        except requests.exceptions.ConnectionError:
            print('проверка соединения')
            time.sleep(60)
