## -*- coding: utf-8 -*-
import multiprocessing
import json
import os
import time
from binance import Client

from binance_api import futures_list
from config_handler import TIMEFRAMES, AVG_VOLUMES_FILE, BINANCE_API_KEY, BINANCE_Secret_KEY

THREAD_CNT = 2 # 3 потока на ядро
PAUSE = 5 # пауза между запросами истории
DEBUG = False# флаг вывода отладочных сообщений во время разработки


def GetVolumeListAndAvg(bars):
    _ = []
    avg = 0.0
    for bar in bars:
        val = float(bar[5])
        _.append(val)
        avg += val
    avg = avg/len(bars)
    return avg


def load_history_bars(task):
    """
    Load historical bars
    :return:
    """
    result = dict()
    pair = task[0]
    api_key = task[1]
    secret_key = task[2]
    all_timeframes = task[3]
    client = Client(api_key, secret_key)

    try:
        result['id'] = pair
        for timeframe in all_timeframes :

            if timeframe == '1m':
                st_time = "1 day ago UTC"
            elif timeframe == '5m':
                st_time = "5 day ago UTC"
            elif timeframe == '10m':
                st_time = "5 day ago UTC"
            elif timeframe == '15m':
                st_time = "5 day ago UTC"
            elif timeframe == '30m':
                st_time = "5 day ago UTC"
            elif timeframe == '1h':
                st_time = "2 day ago UTC"
            elif timeframe == '2h':
                st_time = "2 day ago UTC"
            elif timeframe == '4h':
                st_time = "4 day ago UTC"
            elif timeframe == '1d':
                st_time = "20 day ago UTC"
            else:
                print('Unknows timeframe:', timeframe)
                continue

            bars = []
            try:
                bars = client.get_historical_klines(pair, timeframe, st_time)
            except Exception as e:
                print(pair,':', e)

            if len(bars) == 0:
                print(f" 0 bars has been gethered from server. client.get_historical_klines({pair}, {timeframe}, "
                      f"{st_time})")
                result[timeframe] = 0
                continue
            avg = GetVolumeListAndAvg(bars)
            result[timeframe] = round(avg, 2) #float("{0.2f}".format(avg))
        print(result)
        time.sleep(PAUSE)
        return result
    except Exception as e:
        print("Exception when calling load_history_bars: ", e)
        return None


def load_history_bars_end(responce_list):
    data = dict()
    for responce in responce_list:
        id = responce['id']
        del responce['id']
        data[id] = responce
    # print(data)
    try:
        with open(AVG_VOLUMES_FILE, 'w', encoding='cp1251') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))
            print('Avg volumes stored to file')
        avg_volumes = load_avg_volume_params(AVG_VOLUMES_FILE)
    except Exception as e:
        print("Avg volumes loading exception:", e)


def load_avg_volume_params(file):
    if os.path.isfile(file) is False: # file not exists
        print(f'Avg volumes file  "{file}" not exists.')
        return None
    pairs = []
    try:
        with open(file, 'r', encoding='cp1251') as f:
            avg_volumes = json.load(f)
        print('Volumes loaded.')
        return avg_volumes
    except Exception as e:
        print("load_avg_volume_params exception:", e)
        return None


def update_avg_volumes(timeframes):
    tasks = []

    for symbol in futures_list:
        tasks.append((symbol, BINANCE_API_KEY, BINANCE_Secret_KEY, timeframes))

    try:
        with multiprocessing.Pool(multiprocessing.cpu_count() * THREAD_CNT) as pool:
            pool.map_async(load_history_bars, tasks, callback=load_history_bars_end)
            pool.close()
            pool.join()
    except Exception as ex:
        print("update_avg_volumes exception:", ex)
        return



def load_futures_list():
    client = Client(BINANCE_API_KEY, BINANCE_Secret_KEY)
    futures_info_list = client.futures_exchange_info()
    futures = []
    for item in futures_info_list['symbols']:
        if item['status'] != 'TRADING': continue
        futures.append(item['pair'])
    return futures


def main():

    if os.path.isfile(AVG_VOLUMES_FILE) is False:  # avg volumes file don't exists
        # get avg volumes for every timeframe
        update_avg_volumes(TIMEFRAMES)
    elif os.path.getsize(AVG_VOLUMES_FILE) == 0:
        update_avg_volumes(TIMEFRAMES)


if __name__ == '__main__':
    main()