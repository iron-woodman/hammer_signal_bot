## -*- coding: utf-8 -*-
from binance import ThreadedWebsocketManager, enums
import threading
from time import sleep

from signal_logic import check_bar_for_signal
from telegram_api import add_signal_to_list
import logger as custom_logging


# WEBSOCKET_URL_FUTURES = "wss://fstream.binance.com/stream"


class QueueManager():
    def __init__(self, symbols: list = [], timeframes: list = []) -> None:
        self._twm = ThreadedWebsocketManager()
        self._streams = []
        for symbol in symbols:
            for timeframe in timeframes:
                self._streams.append(f"{symbol.replace('/', '').lower()}@kline_{timeframe}")

        self._twm.start()
        custom_logging.warning(f"Start listening to {len(self._streams)} streams")
        self._listener: str = self._twm.start_futures_multiplex_socket(callback=self._handle_socket_message,
                                                                       streams=self._streams,
                                                                       futures_type=enums.FuturesType.USD_M)

    def _handle_socket_message(self, message):
        if ('e' in message):
            if (message['m'] == 'Queue overflow. Message not filled'):
                custom_logging.warning("Socket queue full. Resetting connection.")
                self.reset_socket()
                return
            else:
                custom_logging.error(f"Stream error: {message['m']}")
                exit(1)
        try:

            if 'stream' in message and 'data' in message:
                json_message = message['data']
                symbol = json_message['s']
                candle = json_message['k']
                is_candle_closed = candle[
                    'x']  # True -свеча сформировалась (закрыта), False - еще формируется (открыта)
                open_ = float(candle['o'])
                high = float(candle['h'])
                low = float(candle['l'])
                close = float(candle['c'])
                volume = float(candle['v'])
                timeframe = candle['i']
                candle_time = candle['t']

                if is_candle_closed:
                    signal = ''
                    signal = check_bar_for_signal(symbol, open_, high, low, close, volume, timeframe)
                    if signal != '':
                        # print(signal)
                        # send_signal(signal)
                        add_signal_to_list(signal)


        except Exception as e:
            print("on_message exception:", e)
            custom_logging.error("on_message exception:", e)
        # print(message)

        if False:
            # in case your internal logic invalidates the items in the queue
            # (e.g. your business logic ran too long and items in queue became "too old")
            reset_socket()

    def reset_socket(self):
        self._twm.stop_socket(self._listener)
        self._listener = self._twm.start_multiplex_socket(callback=self._handle_socket_message,
                                                          streams=self._streams)
        custom_logging.warning("Reconnecting. Waiting for 5 seconds...")
        sleep(5)

    def join(self):
        self._twm.join()
