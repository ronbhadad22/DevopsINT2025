import requests
from collections import defaultdict
import re
from datetime import datetime
import time
from yt_dlp import YoutubeDL
from python_katas.kata_3.utils import open_img, save_img

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# -------------------- 5 Kata --------------------
def knapsack(items, knapsack_limit=50):
    """
    0/1 Knapsack: choose items with max value, under weight limit
    items: dict {name: (weight, value)}
    return: set of chosen item names
    """
    names = list(items.keys())
    weights = [items[n][0] for n in names]
    values = [items[n][1] for n in names]
    n = len(names)

    # DP table
    dp = [[0] * (knapsack_limit + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for cap in range(1, knapsack_limit + 1):
            if w <= cap:
                dp[i][cap] = max(dp[i - 1][cap], dp[i - 1][cap - w] + v)
            else:
                dp[i][cap] = dp[i - 1][cap]

    # backtrack
    res = set()
    cap = knapsack_limit
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            res.add(names[i - 1])
            cap -= weights[i - 1]
    return res


# -------------------- 2 Kata --------------------
def time_me(func):
    runs = 100
    total_time = 0.0
    for _ in range(runs):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / runs


# -------------------- 3 Kata --------------------
def youtube_download(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# -------------------- 5 Kata --------------------
def tasks_scheduling(tasks):
    indexed_tasks = list(enumerate(tasks))
    indexed_tasks.sort(key=lambda x: x[1][1])

    selected = []
    current_end = None
    for idx, (start, end) in indexed_tasks:
        if current_end is None or start >= current_end:
            selected.append(idx)
            current_end = end
    return sorted(selected)


# -------------------- 5 Kata --------------------
def valid_dag(edges):
    """Return True if edges form a valid DAG (no cycles)."""
    graph = defaultdict(list)
    indegree = defaultdict(int)

    nodes = set()
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1
        nodes.add(u)
        nodes.add(v)

    # Kahn's algorithm
    queue = [n for n in nodes if indegree[n] == 0]
    visited = 0

    while queue:
        node = queue.pop(0)
        visited += 1
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    return visited == len(nodes)


# -------------------- 3 Kata --------------------
def rotate_img(img_filename):
    image = open_img(img_filename)
    rotated_img = [list(row) for row in zip(*image[::-1])]
    save_img(rotated_img, f'rotated_{img_filename}')


# -------------------- 4 Kata --------------------
def img_blur(img_filename):
    image = open_img(img_filename)
    height, width = len(image), len(image[0])
    blurred_img = [[None] * width for _ in range(height)]

    for i in range(height):
        for j in range(width):
            neighbors = []
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width:
                        neighbors.append(image[ni][nj])
            avg_pixel = tuple(
                sum(p[k] for p in neighbors) // len(neighbors)
                for k in range(len(neighbors[0]))
            )
            blurred_img[i][j] = avg_pixel

    save_img(blurred_img, f'blured_{img_filename}')


# -------------------- 3 Kata --------------------
def apache_logs_parser(apache_single_log):
    pattern = re.compile(
        r"\[(?P<date>[^\]]+)\]\s"
        r"\[[^:]+:(?P<level>[^\]]+)\]\s"
        r"\[pid\s(?P<pid>\d+):tid\s(?P<tid>\d+)\]\s"
        r"\[client\s(?P<ip>[^\]]+)\]\s"
        r"(?P<message>.*)"
    )
    match = pattern.match(apache_single_log)
    if not match:
        raise ValueError("Log line doesn't match format")

    date_str = match.group("date")
    date = datetime.strptime(date_str, "%a %b %d %H:%M:%S.%f %Y")

    return (
        date,
        match.group("level"),
        int(match.group("pid")),
        int(match.group("tid")),
        match.group("ip"),
        match.group("message"),
    )


# -------------------- 2 Kata --------------------
def simple_http_request():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# -------------------- 8 Kata --------------------
class SortedDict(dict):
    def keys(self):
        return sorted(super().keys())

    def items(self):
        return [(k, self[k]) for k in self.keys()]

    def values(self):
        return [self[k] for k in self.keys()]


# -------------------- 8 Kata --------------------
class CacheList(list):
    def __init__(self, cache_size=5):
        super().__init__()
        self.cache_size = cache_size

    def append(self, element):
        if len(self) >= self.cache_size:
            self.pop(0)
        super().append(element)


# -------------------- Main --------------------
if __name__ == '__main__':
    from random import random

    print('\nknapsack\n--------------------')
    res = knapsack({
        'book': (3, 2),
        'television': (4, 3),
        'table': (6, 1),
        'scooter': (5, 4)
    }, knapsack_limit=8)
    print(res)

    print('\ntime_me\n--------------------')
    time_took = time_me(lambda: sum(range(1000)))
    print(time_took)

    # print('\nyoutube_download\n--------------------')
    # youtube_download('Urdlvw0SSEc')

    print('\ntasks_scheduling\n--------------------')
    tasks = tasks_scheduling([
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT))
    ])
    print(tasks)

    print('\nvalid_dag\n--------------------')
    print(valid_dag([('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))
    print(valid_dag([('a', 'b'), ('c', 'a'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))

    # print('\nrotate_img\n--------------------')
    # rotate_img('67203.jpeg')

    # print('\nimg_blur\n--------------------')
    # img_blur('67203.jpeg')

    print('\napache_logs_parser\n--------------------')
    log_line = '[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico'
    print(apache_logs_parser(log_line))

    print('\nsimple_http_request\n--------------------')
    info = simple_http_request()
    print("Binance symbols count:", len(info["symbols"]))

    print('\nSortedDict\n--------------------')
    s_dict = SortedDict()
    s_dict['a'] = 1
    s_dict['t'] = 2
    s_dict['h'] = 3
    s_dict['q'] = 4
    s_dict['b'] = 5
    print(s_dict.items())

    print('\nCacheList\n--------------------')
    c_list = CacheList(5)
    for i in range(1, 7):
        c_list.append(i)
    print(c_list)
