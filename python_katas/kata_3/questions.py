import time
import requests
from statistics import mean


def time_me(func):
    """
    2 Kata
    Execute func 100 times and return the mean execution time in seconds.
    """
    times = []
    for _ in range(100):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)
    return mean(times)


def simple_http_request():
    """
    2 Kata
    Returns Binance market data JSON by performing a simple HTTP request
    to '/api/v3/exchangeInfo' endpoint.
    """
    url = "https://api.binance.com/api/v3/exchangeInfo"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()
