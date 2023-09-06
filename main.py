## -*- coding: utf-8 -*-
from time import sleep
import threading

from config_handler import TIMEFRAMES
import logger as custom_logging
from binance_api import futures_list
from websocket_handler import QueueManager
from telegram_api import send_signal, send_signals_pack


def main():
    custom_logging.info(f"Bot started.")
    custom_logging.info(f"Coin list loaded ({len(futures_list)})")
    print(f"Coin list count {len(futures_list)}.")
    send_signal(f'HammerBot started. Coins count: {len(futures_list)}. TF:{TIMEFRAMES}.')
    if len(futures_list) == 0:
        exit(1)

    tlg_message_sender = threading.Thread(target=send_signals_pack)
    tlg_message_sender.start()

    manager = QueueManager(symbols=futures_list, timeframes=TIMEFRAMES)
    manager.join()


if __name__ == "__main__":
    main()
