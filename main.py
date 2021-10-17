import os
import time
from textwrap import dedent
import logging

import requests
import telegram
from dotenv import load_dotenv


def send_telegram_message(devman_lesson, bot, chat_id):
    for lesson in devman_lesson['new_attempts']:
        accept_work = lesson['is_negative']
        lesson_title = lesson['lesson_title']
        lesson_url = lesson['lesson_url']
        full_lesson_url = f'https://dvmn.org{lesson_url}'
        if accept_work:
            message = f'''\
            У вас проверили работу "{lesson_title}"\n
            К сожеление, в работе нашлись ошибки.
            {full_lesson_url}
            '''
        else:
            message = f'''\
            У вас проверили работу "{lesson_title}"\n
            Преподователю все понравилось можно приступить к\
            следующему уроку.'''
        bot.send_message(text=dedent(message), chat_id=chat_id)


def get_works_result(devman_token, telegram_bot, telegram_chat_id,
                     timestamp=None):
    logging.warning('Бот запущен')
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': devman_token}
    while True:
        try:
            payload = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, params=payload,
                                    timeout=60)
            response.raise_for_status()
            lesson = response.json()
            status = lesson['status']
            if status == 'timout':
                timestamp = lesson['timestamp_to_request']
            elif status == 'found':
                timestamp = lesson['last_attempt_timestamp']
                send_telegram_message(lesson, telegram_bot, telegram_chat_id)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('проверка соединения')
            time.sleep(60)

if __name__ == '__main__':
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    telegram_bot = telegram.Bot(token=telegram_token)

    get_works_result(devman_token, telegram_bot,
                             telegram_chat_id)

