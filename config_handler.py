## -*- coding: utf-8 -*-
import json
import os
import logger as custom_logging


DEBUG = False
common_params = dict()


def load_common_params(file):
    if os.path.exists(file) is False:
        print(f'File {file} not exists.')
        custom_logging.errr(f"File {file} not exist'.")
        return None

    with open(file, 'r') as f:
        params = json.load(f)
        custom_logging.info(f"***************************************************************************")
        custom_logging.info(f"Params loaded from file '{file}'.")

    return params


if DEBUG:
    common_params = load_common_params('config/common_params_debug.json')
else:
    common_params = load_common_params('config/common_params.json')


BINANCE_API_KEY = common_params['API_Key']
BINANCE_Secret_KEY = common_params['Secret_Key']
TLG_TOKEN = common_params['telegram_token']
TLG_CHANNEL_ID = common_params['telegram_channel_id']
TIMEFRAMES = common_params['timeframes']
AVG_VOLUMES_FILE = common_params['avg_volumes_file']


