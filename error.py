Your code is similar to python-binance-1.0.17. I think your VPS doesn't understand the encoding well.     

def _get_futures_socket(self, path: str, futures_type: FuturesType, prefix: str = 'stream?streams='):
        socket_type: BinanceSocketType = BinanceSocketType.USD_M_FUTURES
        if futures_type == FuturesType.USD_M:
            stream_url = self.FSTREAM_URL
            if self.testnet:
                stream_url = self.FSTREAM_TESTNET_URL
        else:
            stream_url = self.DSTREAM_URL