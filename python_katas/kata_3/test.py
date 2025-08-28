import unittest
from python_katas.kata_3 import questions
from python_katas.utils import unittest_runner



import unittest

class TestKnapsack(unittest.TestCase):
    """
    Knapsack Test
    """

    def test_sample(self):
        # Sample data
        items = {
            "item1": (2, 3),   # weight 2, value 3
            "item2": (3, 4),   # weight 3, value 4
            "item3": (4, 5),   # weight 4, value 5
        }
        knapsack_limit = 5

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

        # Backtrack to find selected items
        res = set()
        cap = knapsack_limit
        for i in range(n, 0, -1):
            if dp[i][cap] != dp[i - 1][cap]:
                res.add(names[i - 1])
                cap -= weights[i - 1]

        # Assert results
        self.assertIsInstance(res, set)
        # Check that the total weight does not exceed limit
        total_weight = sum(items[n][0] for n in res)
        self.assertLessEqual(total_weight, knapsack_limit)
        # Optional: check expected max value
        total_value = sum(items[n][1] for n in res)
        self.assertEqual(total_value, 7)  # optimal selection: item1 + item2

if __name__ == "__main__":
    unittest.main()



class TestTimeMe(unittest.TestCase):
    """
    2 Kata
    """
    def test_sample(self):
        # your code here
        pass


import unittest
from yt_dlp import YoutubeDL  # Make sure yt-dlp is installed

# The function to download a video
def youtube_download(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # filename template
        'quiet': True,                    # suppress console output for testing
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Unit test
class TestYoutubeDownload(unittest.TestCase):
    """
    3 Kata
    """
    def test_sample(self):
        # Test that the function runs without throwing an error
        try:
            # Use a small test video ID that is safe to download
            youtube_download("dQw4w9WgXcQ")  # Replace with a valid small video for testing
        except Exception as e:
            self.fail(f"youtube_download raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()




# Function to schedule tasks
def tasks_scheduling(tasks):
    indexed_tasks = list(enumerate(tasks))
    indexed_tasks.sort(key=lambda x: x[1][1])  # sort by end time

    selected = []
    current_end = None
    for idx, (start, end) in indexed_tasks:
        if current_end is None or start >= current_end:
            selected.append(idx)
            current_end = end
    return sorted(selected)

# Unit test class
class TestTasksScheduling(unittest.TestCase):
    """
    5 Kata
    """
    def test_sample(self):
        # Example tasks: (start, end)
        tasks = [(1, 3), (2, 5), (4, 6), (6, 8)]
        result = tasks_scheduling(tasks)
        # Expected selected task indices
        expected = [0, 2, 3]  # tasks[0], tasks[2], tasks[3]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()



class TestValidDag(unittest.TestCase):
    """
    5 Kata
    """
    def test_sample(self):
        # your code here
        pass


class TestRotateImg(unittest.TestCase):
    """
    3 Kata
    """
    def test_sample(self):
        # your code here
        pass


class TestImgBlur(unittest.TestCase):
    """
    4 Kata
    """
    def test_sample(self):
        # your code here
        pass


class TestApacheLogsParser(unittest.TestCase):
    """
    3 Kata
    """
    def test_sample(self):
        # your code here
        pass


class TestSimpleHttpRequest(unittest.TestCase):
    """
    2 Kata
    """
    def test_sample(self):
        # your code here
        pass


if __name__ == '__main__':
    import inspect
    import sys
    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))
# test_questions.py
import pytest
from datetime import datetime
from python_katas.kata_3.questions import (
    knapsack, time_me, tasks_scheduling, valid_dag,
    apache_logs_parser, simple_http_request,
    SortedDict, CacheList
)

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# -------------------- knapsack --------------------
def test_knapsack():
    items = {
        'book': (3, 2),
        'television': (4, 3),
        'table': (6, 1),
        'scooter': (5, 4)
    }
    res = knapsack(items, 8)
    # best is book(2) + scooter(4) = 6 value
    assert res == {'book', 'scooter'}


# -------------------- time_me --------------------
def test_time_me_runs_and_returns_float():
    def dummy():
        sum(range(10))
    avg_time = time_me(dummy)
    assert isinstance(avg_time, float)
    assert avg_time >= 0


# -------------------- tasks_scheduling --------------------
def test_tasks_scheduling():
    tasks = [
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT))
    ]
    result = tasks_scheduling(tasks)
    assert isinstance(result, list)
    # should include earliest non-overlapping ones
    assert 5 in result  # 10:00 - 10:10
    assert 0 in result  # 13:00 - 14:00
    assert 3 in result  # 14:00 - 14:05


# -------------------- valid_dag --------------------
def test_valid_dag_true():
    edges = [('a', 'b'), ('a', 'c'), ('b', 'd')]
    assert valid_dag(edges) is True


def test_valid_dag_false_cycle():
    edges = [('a', 'b'), ('b', 'a')]
    assert valid_dag(edges) is False


# -------------------- apache_logs_parser --------------------
def test_apache_logs_parser_valid():
    log_line = '[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico'
    parsed = apache_logs_parser(log_line)
    assert isinstance(parsed[0], datetime)
    assert parsed[1] == "error"
    assert parsed[2] == 35708
    assert parsed[4] == "72.15.99.187"


def test_apache_logs_parser_invalid():
    with pytest.raises(ValueError):
        apache_logs_parser("invalid log line")


# -------------------- simple_http_request --------------------
def test_simple_http_request(monkeypatch):
    class DummyResponse:
        def raise_for_status(self): pass
        def json(self): return {"symbols": [1, 2, 3]}

    def dummy_get(url): return DummyResponse()

    import python_katas.kata_3.questions as q
    monkeypatch.setattr(q.requests, "get", dummy_get)

    data = simple_http_request()
    assert "symbols" in data
    assert len(data["symbols"]) == 3


# -------------------- SortedDict --------------------
def test_sorteddict():
    d = SortedDict()
    d["z"] = 1
    d["a"] = 2
    d["m"] = 3
    assert d.keys() == ["a", "m", "z"]
    assert d.values() == [2, 3, 1]
    assert d.items() == [("a", 2), ("m", 3), ("z", 1)]


# -------------------- CacheList --------------------
def test_cachelist_respects_size():
    cl = CacheList(cache_size=3)
    cl.append(1)
    cl.append(2)
    cl.append(3)
    cl.append(4)  # should drop 1
    assert cl == [2, 3, 4]
    cl.append(5)
    assert cl == [3, 4, 5]
