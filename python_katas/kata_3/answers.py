
from python_katas.kata_3.utils import open_img, save_img
import requests   # to be used in simple_http_request()
import time
import re
from statistics import mean
from typing import Dict, Tuple, List, Any, Set
from collections import defaultdict, deque

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def knapsack(items: Dict[str, Tuple[int, int]], knapsack_limit: int = 50) -> Set[str]:
    """
    5 Kata

    Given a set of items, dict of tuples representing the (weight, value),
    determine the items to include so that the total weight is <= limit and total value is maximal.

    Classic 0/1 knapsack dynamic programming implementation that returns the chosen item names.
    """
    names = list(items.keys())
    n = len(names)
    weights = [items[name][0] for name in names]
    values = [items[name][1] for name in names]

    # dp[w] = (value, chosen_set_indices)
    dp = [(0, set()) for _ in range(knapsack_limit + 1)]

    for i in range(n):
        w_i, v_i = weights[i], values[i]
        # iterate backwards on capacity
        for w in range(knapsack_limit, w_i - 1, -1):
            prev_val, prev_set = dp[w - w_i]
            cand_val = prev_val + v_i
            if cand_val > dp[w][0]:
                new_set = prev_set.copy()
                new_set.add(i)
                dp[w] = (cand_val, new_set)

    # choose best by value among capacities
    best_val, best_set = max(dp, key=lambda t: t[0])
    return {names[i] for i in best_set}


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


def youtube_download(video_id: str):
    """
    3 Kata

    Download a YouTube video by its video_id using yt_dlp (a maintained fork of youtube-dl).
    Saves the best available format into the current working directory.

    Requires: pip install yt_dlp
    """
    try:
        import yt_dlp  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "yt_dlp is required for youtube_download(). Install with: pip install yt_dlp"
        ) from e

    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def tasks_scheduling(tasks: List[Tuple[Any, Any]]) -> List[int]:
    """
    5 Kata

    Interval scheduling maximization: select the maximum number of non-overlapping tasks.
    Returns the list of original indices to perform (sorted by finishing time selection).
    """
    indexed = [(i, s, e) for i, (s, e) in enumerate(tasks)]
    # sort by end time
    indexed.sort(key=lambda t: t[2])
    chosen: List[int] = []
    last_end = None
    for i, s, e in indexed:
        if last_end is None or s >= last_end:
            chosen.append(i)
            last_end = e
    return chosen


def valid_dag(edges: List[Tuple[str, str]]) -> bool:
    """
    5 Kata

    Determine whether the directed graph defined by 'edges' is a DAG.
    Uses Kahn's algorithm for topological sorting.
    """
    # collect nodes
    nodes = set()
    for u, v in edges:
        if u == v:
            return False  # self loop => cycle
        nodes.add(u)
        nodes.add(v)

    adj = defaultdict(list)
    indeg = defaultdict(int)
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
        indeg.setdefault(u, 0)

    # Kahn's algorithm
    q = deque([n for n in nodes if indeg[n] == 0])
    visited = 0
    while q:
        u = q.popleft()
        visited += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return visited == len(nodes)


def _rotate_matrix_clockwise(matrix: List[List[Any]]) -> List[List[Any]]:
    # matrix is list of rows; rotate clockwise -> transpose + reverse rows of original
    # Equivalent to zip(*matrix[::-1]) but convert tuples back to lists
    return [list(row) for row in zip(*matrix[::-1])]


def rotate_img(img_filename: str):
    """
    3 Kata

    Rotates image clockwise and saves as 'rotated_<original filename>'.
    Expects open_img/save_img from python_katas.kata_3.utils to work with list-of-lists of pixels.
    """
    image = open_img(img_filename)
    rotated_img = _rotate_matrix_clockwise(image)
    save_img(rotated_img, f'rotated_{img_filename}')


def _neighbors(i: int, j: int, h: int, w: int):
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w:
                yield ni, nj


def img_blur(img_filename: str):
    """
    4 Kata

    Blurs an image (each pixel becomes the average of itself and its 8-neighbors within bounds).
    Saves as 'blured_<original filename>'.
    """
    image = open_img(img_filename)
    h = len(image)
    w = len(image[0]) if h else 0

    blurred = [[None for _ in range(w)] for _ in range(h)]
    for i in range(h):
        for j in range(w):
            # support either grayscale ints or RGB tuples
            pixels = [image[ni][nj] for ni, nj in _neighbors(i, j, h, w)]
            sample = pixels[0]
            if isinstance(sample, (tuple, list)) and len(sample) in (3, 4):
                # color image (RGB or RGBA)
                channels = len(sample)
                sums = [0] * channels
                for p in pixels:
                    for c in range(channels):
                        sums[c] += p[c]
                cnt = len(pixels)
                avg = tuple(int(round(s / cnt)) for s in sums)
                blurred[i][j] = avg
            else:
                # grayscale
                avg = int(round(sum(pixels) / len(pixels)))
                blurred[i][j] = avg

    save_img(blurred, f'blured_{img_filename}')


_APACHE_RE = re.compile(
    r"""^\[(?P<date>.+?)\]\s+\[(?P<level>[^\]]+)\]\s+\[pid\s+(?P<pid>\d+):tid\s+(?P<tid>\d+)\]\s+\[client\s+(?P<ip>[\d\.]+)\]\s+(?P<msg>.*)$"""
)


def apache_logs_parser(apache_single_log: str):
    """
    3 Kata

    Parses apache error log line into components:
    date (str as in the log; convert upstream to datetime if desired), level, pid, tid, client_ip, log message.
    """
    m = _APACHE_RE.match(apache_single_log.strip())
    if not m:
        raise ValueError("Log line does not match expected Apache error log format")
    date = m.group("date")
    level = m.group("level")
    pid = int(m.group("pid"))
    tid = int(m.group("tid"))
    client_ip = m.group("ip")
    log = m.group("msg")
    return date, level, pid, tid, client_ip, log


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


class SortedDict(dict):
    """
    8 Kata

    A dictionary whose view methods (keys, values, items) are returned in key-sorted order.
    Also allows attribute-style set/get for simple identifiers (e.g., d.apple = 'aaa').
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        # fallback to dict item if not a real attribute
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(key) from e

    def __setattr__(self, key, value):
        # allow normal attribute setting for dunder/private/internal attributes
        if key.startswith("_") or key in ("clear", "copy", "fromkeys", "get", "items",
                                          "keys", "pop", "popitem", "setdefault",
                                          "update", "values"):
            return super().__setattr__(key, value)
        # otherwise store as a dict key
        self[key] = value

    def items(self):
        return [(k, self[k]) for k in sorted(super().keys())]

    def values(self):
        return [self[k] for k in sorted(super().keys())]

    def keys(self):
        return list(sorted(super().keys()))


class CacheList(list):
    """
    8 Kata

    A list that only keeps the last `cache_size` appended elements.
    Older elements are dropped from the left when capacity is exceeded.
    """

    def __init__(self, cache_size: int = 5):
        super().__init__()
        if cache_size <= 0:
            raise ValueError("cache_size must be positive")
        self.cache_size = cache_size

    def append(self, element):
        super().append(element)
        # trim the left side if longer than capacity
        while len(self) > self.cache_size:
            del self[0]


if __name__ == '__main__':
    import time as _t
    from random import random as _random
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
    time_took = time_me(lambda: _t.sleep(0.01 + _random() * 0.02))
    print(time_took)

    print('\nyoutube_download\n--------------------')
    try:
        youtube_download('Urdlvw0SSEc')
        print('Downloaded!')
    except Exception as e:
        print(f'youtube_download skipped: {e}')

    print('\ntasks_scheduling\n--------------------')
    tasks = [
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT))
    ]
    print(tasks_scheduling(tasks))

    print('\nvalid_dag\n--------------------')
    print(valid_dag([('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))
    print(valid_dag([('a', 'b'), ('c', 'a'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))

    print('\nrotate_img\n--------------------')
    # rotate_img('67203.jpeg')  # Uncomment if the file exists

    print('\nimg_blur\n--------------------')
    # img_blur('67203.jpeg')  # Uncomment if the file exists

    print('\napache_logs_parser\n--------------------')
    date, level, pid, tid, client_ip, log = apache_logs_parser('[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico')
    print(date, level, pid, tid, client_ip, log)

    print('\nsimple_http_request\n--------------------')
    try:
        info = simple_http_request()
        print('Symbols count:', len(info.get("symbols", [])))
    except Exception as e:
        print(f'HTTP request skipped/failed: {e}')

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
