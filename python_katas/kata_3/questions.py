import requests
from PIL import Image
from collections import defaultdict
import re
import os
from datetime import datetime
from pytube import YouTube
import time
from python_katas.kata_3.utils import open_img, save_img
import requests   # to be used in simple_http_request()

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def knapsack(items, knapsack_limit=50):
    """
    5 Kata

    Consider a thief gets into a home to rob and he carries a knapsack.
    There are fixed number of items in the home — each with its own weight and value —
    Jewelry, with less weight and highest value vs tables, with less value but a lot heavy.
    To add fuel to the fire, the thief has an old knapsack which has limited capacity.
    Obviously, he can’t split the table into half or jewelry into 3/4ths. He either takes it or leaves it

    Given a set of items, dict of tuples representing the (weight, value), determine the items to include in a collection
    so that the total weight is less than or equal to a given limit and the total value is as large as possible.

    :param items: dict of tuples e.g. {"bed": (100, 15), "iphone13": (1, 1500)}
    :param knapsack_limit:
    :return: set of items
    """

    item_names = list(items.keys())
    weights = [items[name][0] for name in item_names]
    values = [items[name][1] for name in item_names]
    n = len(item_names)

    dp = [[0] * (knapsack_limit + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(knapsack_limit + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[1 - 1][w - weights[i - 1]] + values[i - 1]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    w = knapsack_limit
    selected_items = set()
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.add(item_names[i - 1])
            w -= weights[i - 1]

    return selected_items


def time_me(func):
    """
    2 Kata

    Given func - a pointer to sime function which can be executed by func()
    Return the number of time it took to execute the function. Since execution time may vary from time to time,
    execute func 100 time and return the mean

    :param func:
    :return:
    """

    runs = 100
    total_time = 0

    for _ in range(runs):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        total_time += (end - start)

    return total_time / runs


def youtube_download(video_id):
    """
    3 Kata

    Youtube video url is in the form https://www.youtube.com/watch?v=<video id>
    This function get a youtube video id and downloads this video to the local fs

    hint: https://www.bogotobogo.com/VideoStreaming/YouTube/youtube-dl-embedding.php

    :param video_id: str
    :return: None
    """

    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Failed to download video: {e}")


def tasks_scheduling(tasks):
    """
    5 Kata

    Consider a list of n tasks (tuples), each has starting and ending time (datetime object), as following:
    [(s_1, e_1), (s_2, e_2), ..., (s_n, e_n)]
    where s_* and e_* are Python datetime objects

    Only one task can be performed every time.
    This function returns the index of tasks to perform such the total completed tasks is as large as possible

    :param: tasks: list of tuple (start, end) while start and end are datetime objects
    :return: list of tasks indexes to perform
    """

    indexed_tasks = sorted(enumerate(tasks), key=lambda x: x[1][1])

    selected = []
    last_end_time = None

    for index, (start, end) in indexed_tasks:
        if last_end_time is None or start >= last_end_time:
            selected.append(index)
            last_end_time = end

    return sorted(selected)


def valid_dag(edges):
    """
    5 Kata

    Given a DAG (https://en.wikipedia.org/wiki/Directed_acyclic_graph) in the form:
    [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]

    where a, b, c, d, e are vertices and ('a', 'b') etc... are edges
    This function determine whether the graph is a valid DAG

    :param edges: list of tuples of string 'a', 'b'....
    :return: bool - True if and only if it is a valid DAG
    """

    graph = defaultdict(list)
    nodes = set()

    for src, dst in edges:
        graph[src].append(dst)
        nodes.add(src)
        nodes.add(dst)

    # 0 = unvisited, 1 = visiting, 2 = visited
    state = {node: 0 for node in nodes}

    def has_cycles(node):
        if state[node] == 1:
            return True  # back edge found → cycle
        if state[node] == 2:
            return False  # already processed safely

        state[node] = 1  # mark as visiting
        for neighbor in graph[node]:
            if has_cycles(neighbor):
                return True
        state[node] = 2  # mark as visited
        return False

    for node in nodes:
        if state[node] == 0:
            if has_cycles(node):
                return False  # cycle detected

    return True  # no cycles, valid DAG


def rotate_img(img_filename):
    """
    3 Kata

    Rotates image clockwise

    :param img_filename: image file path (png or jpeg)
    :return: None, the rotated image should be saved as 'rotated_<original image filename>'
    """

    def open_img(filename):
        img = Image.open(filename)
        pixels = list(img.getdata())
        width, height = img.size
        matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]
        return matrix, img.mode, img.size

    def save_img(pixel_matrix, filename, mode, size):
        img = Image.new(mode, size)
        flat_pixels = [pixel for row in pixel_matrix for pixel in row]
        img.putdata(flat_pixels)
        img.save(filename)

    def rotate_matrix(mat):

        return [list(reversed(col)) for col in zip(*mat)]

    image_matrix, mode, size = open_img(img_filename)

    rotated_img = rotate_matrix(image_matrix)

    rotated_size = (size[1], size[0])

    save_img(rotated_img, f'rotated_{img_filename}', mode, rotated_size)


def img_blur(img_filename):
    """
    4 Kata

    Blurs an image (every pixel is an average of its nearest neighbors)

    :param img_filename: image file path (png or jpeg)
    :return: None, the rotated image should be saved as 'rotated_<original image filename>'
    """

    def open_img(filename):
        img = Image.open(filename)
        pixels = list(img.getdata())
        width, height = img.size
        matrix = [pixels[i * width:(i + 1) * width] for i in range(height)]
        return matrix, img.mode, img.size

    def save_img(pixel_matrix, filename, mode, size):
        img = Image.new(mode, size)
        flat_pixels = [pixel for row in pixel_matrix for pixel in row]
        img.putdata(flat_pixels)
        img.save(filename)

    def get_neighbors_avg(matrix, x, y, width, height):
        neighbors = []
        for i in range(max(0, x - 1), min(height, x + 2)):
            for j in range(max(0, y - 1), min(width, y + 2)):
                neighbors.append(matrix[i][j])
            if isinstance(neighbors[0], tuple):
                r = sum(p[0] for p in neighbors) // len(neighbors)
                g = sum(p[1] for p in neighbors) // len(neighbors)
                b = sum(p[2] for p in neighbors) // len(neighbors)
                return (r, g, b)
            else:
                return sum(neighbors) // len(neighbors)

    image_matrix, mode, (width, height) = open_img(img_filename)

    blurred = [
        [get_neighbors_avg(image_matrix, x, y, width, height)
         for y in range(width)]
        for x in range(height)
    ]

    save_img(blurred, f'blured_{img_filename}', mode, (width, height))

    # use matrix_avg from previous kata 2 or implement....

    # use the below line to save list as image
    # save_img(blured_img, f'blured_{img_filename}')


def apache_logs_parser(apache_single_log):
    """
    3 Kata

    Parses apache log (see format here https://httpd.apache.org/docs/2.4/logs.html)
    e.g.
    [Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico

    the parsed log data should be:
    date (datetime object), level (str), pid (int), thread_id (int), client_ip (str), log (str)

    Hint: use regex

    :param apache_single_log: str
    :return: parsed log data as tuple
    """

    pattern = (
        r'\[([^\]]+)\]'                    # Date string
        # Module:Level (we extract just the level)
        r' \[[^:]+:(\w+)\]'
        r' \[pid (\d+):tid (\d+)\]'        # PID and thread ID
        r' \[client ([^\]]+)\] '           # Client IP
        r'(.+)'                            # Log message
    )

    match = re.match(pattern, apache_single_log)

    if not match:
        raise ValueError("Log format doesn't match")

    date_str, level, pid, tid, client_ip, log = match.groups()

    # Convert date string to datetime object
    date = datetime.strptime(date_str, "%a %b %d %H:%M:%S.%f %Y")

    return date, level, int(pid), int(tid), client_ip, log.strip()


def simple_http_request():
    """
    2 Kata

    This function returns Binance market data JSON by performing a simple HTTP request to '/api/v3/exchangeInfo' endpoint

    Hint: use requests.get(...)
    Hint: Binance api docs https://binance-docs.github.io/apidocs/spot/en/#market-data-endpoints

    :return: json of market exchange information
    """
    url = "https://api.binance.com/api/v3/exchangeInfo"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to fetch data: {response.status_code} - {response.text}")


class SortedDict(dict):
    """
    8 Kata

    Implement SortedDict class which is a regular Python dictionary,
    but the keys are maintained in sorted order

    Usage example:
    x = SortedDict()

    x['banana'] = 'ccc'
    x['apple'] = 'aaa'
    x['orange'] = 'bbb'

    list(x.keys())
    >> ['apple', 'banana', 'orange']

    list(x.values())
    >> ['aaa', 'ccc', 'bbb']

    list(x.items())
    >> [('apple', 'aaa'), ('banana', 'ccc'), ('orange', 'bbb')]
    """

    def __init__(self):
        super().__init__()
        
    def __setitem__(self, key, value):
        # Regular set item (dict handles storage)
        super().__setitem__(key, value)

    def keys(self):
        # Return keys sorted
        return sorted(super().keys())

    def values(self):
        # Return values based on sorted keys
        return [self[key] for key in self.keys()]

    def items(self):
        # Return key-value pairs based on sorted keys
        return [(key, self[key]) for key in self.keys()]


class CacheList(list):
    """
    8 Kata

    Implement CacheList class which is a regular Python list,
    but it holds the last n elements only (old elements will be deleted)

    Usage example:
    x = CacheList(3)

    x.append(1)
    x.append(2)
    x.append(3)

    print(x)
    >> [1, 2, 3]

    x.append(1)
    print(x)
    >> [2, 3, 1]

    x.append(1)
    print(x)
    >> [3, 1, 1]
    """

    def __init__(self, cache_size=5):
        super().__init__()
        self.cache_size = cache_size  # Store the max size

    def append(self, element):
        if len(self) >= self.cache_size:
            self.pop(0)  # Remove the oldest item
        super().append(element)


if __name__ == '__main__':
    import time
    from random import random
    from datetime import datetime

    print('\nknapsack\n--------------------')
    res = knapsack({
        'book': (3, 2),
        'television': (4, 3),
        'table': (6, 1),
        'scooter': (5, 4)
    }, knapsack_limit=8)
    print(res)

    print('\ntime_me\n--------------------')
    time_took = time_me(lambda: time.sleep(5 + random()))
    print(time_took)

    print('\nyoutube_download\n--------------------')
    youtube_download('Urdlvw0SSEc')

    print('\ntasks_scheduling\n--------------------')
    tasks = tasks_scheduling([
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT),
         datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT),
         datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT),
         datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT),
         datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT),
         datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT),
         datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT))
    ])
    print(tasks)

    print('\nvalid_dag\n--------------------')

    # valid
    print(valid_dag([('a', 'b'), ('a', 'c'), ('a', 'd'),
          ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))

    # invalid
    print(valid_dag([('a', 'b'), ('c', 'a'), ('a', 'd'),
          ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))

    print('\nrotate_img\n--------------------')
    rotate_img('67203.jpeg')

    print('\nimg_blur\n--------------------')
    img_blur('67203.jpeg')

    print('\napache_logs_parser\n--------------------')
    date, level, pid, tid, client_ip, log = apache_logs_parser(
        '[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico')
    print(date, level, pid, tid, client_ip, log)

    print('\nsimple_http_request\n--------------------')
    info = simple_http_request()

    print('\nSortedDict\n--------------------')
    s_dict = SortedDict()
    s_dict['a'] = None
    s_dict['t'] = None
    s_dict['h'] = None
    s_dict['q'] = None
    s_dict['b'] = None
    print(s_dict.items())

    print('\nCacheList\n--------------------')
    c_list = CacheList(5)
    c_list.append(1)
    c_list.append(2)
    c_list.append(3)
    c_list.append(4)
    c_list.append(5)
    c_list.append(6)
    print(c_list)
