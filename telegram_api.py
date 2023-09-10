## -*- coding: utf-8 -*-
import requests
from datetime import datetime
from config_handler import TLG_TOKEN, TLG_CHANNEL_ID
import time

import logger as custom_logging

signals_list = []
last_signal_time = 1.0


def send_signal(signal):
    print("*" * 30 + "\n" + signal)
    custom_logging.info("\n" + signal)
    url = "https://api.telegram.org/bot"
    url += TLG_TOKEN
    method = url + "/sendMessage"
    attemts_count = 5

    while (attemts_count > 0):
        r = requests.post(method, data={
            "chat_id": TLG_CHANNEL_ID,
            "text": signal,
            "parse_mode": "Markdown"
        })

        if r.status_code == 200:
            return
        elif r.status_code != 200:
            print(f'Telegram send signal error ({signal}). Status code={r.status_code}. Text="{r.text}".')
            custom_logging.error(f'Telegram send signal error:\n ({signal}). \nAttempts count={attemts_count}')
            time.sleep(1)
            attemts_count -= 1


def send_signal_list(signal_list):
    for signal in signal_list:
        try:
            send_signal(signal)
        except Exception as e:
            print(e)
            continue



def list_to_long_messages(lst):
    '''
    group signal list into bulk signals
    :param lst:
    :return:
    '''
    long_messages = []
    mess = ''
    for item in lst:
        if len(mess + '\n' + item + '\n') >= 4096: # telegram bot message limit = 4096
            long_messages.append(mess)
            mess = ''
        mess += '\n' + item + '\n'
    long_messages.append(mess)

    return long_messages


def send_signals_pack():
    global last_signal_time
    global signals_list
    while True:
        if time.time() - last_signal_time > 5:
            if len(signals_list) > 0:
                long_messages = list_to_long_messages(signals_list)
                signals_list.clear()
                send_signal_list(long_messages)
                last_signal_time = time.time()
        time.sleep(1)


def add_signal_to_list(signal):
    global signals_list
    global last_signal_time
    signals_list.append(signal)
    last_signal_time = time.time()
