## -*- coding: utf-8 -*-
from binance import Client
import logger as custom_logging
import logging
from config_handler import BINANCE_API_KEY, BINANCE_Secret_KEY


def load_futures_list():
    futures = []

    try:
        client = Client(BINANCE_API_KEY, BINANCE_Secret_KEY)
        futures_info_list = client.futures_exchange_info()
        for item in futures_info_list['symbols']:
            if item['status'] != 'TRADING': continue
            futures.append(item['pair'])
    except Exception as e:
        custom_logging.add_log(f"load_futures_list exception: {e}", level=logging.ERROR)
    return futures


futures_list = load_futures_list()



