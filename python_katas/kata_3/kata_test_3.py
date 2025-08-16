import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
import types
from datetime import datetime
from python_katas.kata_3 import kata_questions_3 as questions


class TestKnapsack(unittest.TestCase):
    """
    5 Kata
    """
    def test_basic_choices(self):
        items = {
            "book": (3, 2),
            "television": (4, 3),
            "table": (6, 1),
            "scooter": (5, 4),
        }
        res = questions.knapsack(items, knapsack_limit=8)
        # Best value is 6 with weight 8: television(4,3) + scooter(5,4) is overweight (9)
        # book(3,2) + scooter(5,4) -> weight 8, value 6  ✅
        # television(4,3) + book(3,2) -> weight 7, value 5
        self.assertEqual(res, {"book", "scooter"})

    def test_zero_capacity(self):
        self.assertEqual(questions.knapsack({"a": (1, 100)}, 0), set())


class TestTimeMe(unittest.TestCase):
    """
    2 Kata
    """
    def test_returns_mean_seconds(self):
        # a no-op function should run very fast; just check type & bounds
        def noop():
            return None
        t = questions.time_me(noop)
        self.assertIsInstance(t, float)
        self.assertGreaterEqual(t, 0.0)
        self.assertLess(t, 0.1)


class TestYoutubeDownload(unittest.TestCase):
    """
    3 Kata
    """
    def test_download_called_when_yt_dlp_present(self):
        # simulate yt_dlp module presence with a dummy YoutubeDL
        called = {"urls": None}

        class DummyYDL:
            def __init__(self, opts):
                self.opts = opts
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                return False
            def download(self, urls):
                called["urls"] = urls

        dummy_mod = types.ModuleType("yt_dlp")
        dummy_mod.YoutubeDL = DummyYDL

        old = sys.modules.get("yt_dlp")
        sys.modules["yt_dlp"] = dummy_mod
        try:
            questions.youtube_download("VIDEOID123")
            self.assertEqual(called["urls"], ["https://www.youtube.com/watch?v=VIDEOID123"])
        finally:
            if old is None:
                del sys.modules["yt_dlp"]
            else:
                sys.modules["yt_dlp"] = old

    def test_graceful_when_yt_dlp_missing(self):
        # Should not raise if yt_dlp can't be imported
        if "yt_dlp" in sys.modules:
            del sys.modules["yt_dlp"]
        self.assertIsNone(questions.youtube_download("ANY"))


class TestTasksScheduling(unittest.TestCase):
    """
    5 Kata
    """
    def test_activity_selection(self):
        ISO = '%Y-%m-%dT%H:%M:%SZ'
        tasks = [
            (datetime.strptime('2022-01-01T13:00:00Z', ISO), datetime.strptime('2022-01-01T14:00:00Z', ISO)),  # 0
            (datetime.strptime('2022-01-01T13:00:00Z', ISO), datetime.strptime('2022-01-01T14:30:00Z', ISO)),  # 1
            (datetime.strptime('2022-01-01T11:00:00Z', ISO), datetime.strptime('2022-01-01T16:00:00Z', ISO)),  # 2
            (datetime.strptime('2022-01-01T14:00:00Z', ISO), datetime.strptime('2022-01-01T14:05:00Z', ISO)),  # 3
            (datetime.strptime('2022-01-01T12:00:00Z', ISO), datetime.strptime('2022-01-01T13:30:00Z', ISO)),  # 4
            (datetime.strptime('2022-01-01T10:00:00Z', ISO), datetime.strptime('2022-01-01T10:10:00Z', ISO)),  # 5
        ]
        chosen = questions.tasks_scheduling(tasks)
        # One optimal set by earliest finishing: [5, 4, 0, 3] (indexes by original order)
        self.assertEqual(chosen, [5, 4, 0, 3])


class TestValidDag(unittest.TestCase):
    """
    5 Kata
    """
    def test_valid(self):
        edges = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]
        self.assertTrue(questions.valid_dag(edges))

    def test_cycle(self):
        edges = [('a', 'b'), ('c', 'a'), ('a', 'c')]  # a->c and c->a makes a cycle
        self.assertFalse(questions.valid_dag(edges))


class TestRotateImg(unittest.TestCase):
    """
    3 Kata
    """
    def test_rotate_calls_save_with_rotated(self):
        # 2x3 matrix
        img = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        saved = {"name": None, "img": None}

        def fake_open(_path):
            return img

        def fake_save(matrix, filename):
            saved["name"] = filename
            saved["img"] = matrix

        # patch in module under test
        orig_open, orig_save = questions.open_img, questions.save_img
        try:
            questions.open_img = fake_open
            questions.save_img = fake_save
            questions.rotate_img("sample.jpeg")
        finally:
            questions.open_img, questions.save_img = orig_open, orig_save

        self.assertEqual(saved["name"], "rotated_sample.jpeg")
        # expected 3x2: columns become rows
        expected = [
            [4, 1],
            [5, 2],
            [6, 3],
        ]
        self.assertEqual(saved["img"], expected)


class TestImgBlur(unittest.TestCase):
    """
    4 Kata
    """
    def test_blur_simple(self):
        # 3x3 simple gradient so averages are easy to check
        img = [
            [0.0, 0.0, 0.0],
            [0.0, 9.0, 0.0],
            [0.0, 0.0, 0.0],
        ]
        captured = {"img": None, "name": None}

        def fake_open(_):
            return img

        def fake_save(m, name):
            captured["img"] = m
            captured["name"] = name

        orig_open, orig_save = questions.open_img, questions.save_img
        try:
            questions.open_img = fake_open
            questions.save_img = fake_save
            questions.img_blur("x.png")
        finally:
            questions.open_img, questions.save_img = orig_open, orig_save

        self.assertEqual(captured["name"], "blured_x.png")
        # center becomes average of all 9 values => 9/9 = 1.0
        self.assertAlmostEqual(captured["img"][1][1], 1.0, places=6)
        # corners average over 4 cells (center + 3 zeros) => 9/4 = 2.25
        self.assertAlmostEqual(captured["img"][0][0], 9.0/4.0, places=6)
        self.assertAlmostEqual(captured["img"][0][2], 9.0/4.0, places=6)
        self.assertAlmostEqual(captured["img"][2][0], 9.0/4.0, places=6)
        self.assertAlmostEqual(captured["img"][2][2], 9.0/4.0, places=6)


class TestApacheLogsParser(unittest.TestCase):
    """
    3 Kata
    """
    def test_parse_sample(self):
        line = ('[Fri Sep 09 10:42:29.902022 2011] [core:error] '
                '[pid 35708:tid 4328636416] [client 72.15.99.187] '
                'File does not exist: /usr/local/apache2/htdocs/favicon.ico')
        dt, level, pid, tid, ip, msg = questions.apache_logs_parser(line)
        self.assertIsInstance(dt, datetime)
        self.assertEqual(level, "error")
        self.assertEqual(pid, 35708)
        self.assertEqual(tid, 4328636416)
        self.assertEqual(ip, "72.15.99.187")
        self.assertTrue(msg.startswith("File does not exist"))


class TestSimpleHttpRequest(unittest.TestCase):
    """
    2 Kata
    """
    def test_success(self):
        class DummyResp:
            def __init__(self): self._json = {"serverTime": 123, "symbols": []}
            def raise_for_status(self): return None
            def json(self): return self._json

        def fake_get(url, timeout=10):
            self.assertIn("/api/v3/exchangeInfo", url)
            return DummyResp()

        orig = questions.requests.get
        try:
            questions.requests.get = fake_get
            data = questions.simple_http_request()
        finally:
            questions.requests.get = orig

        self.assertIsInstance(data, dict)
        self.assertIn("symbols", data)

    def test_failure_returns_none(self):
        def fake_get(_u, timeout=10):
            raise OSError("offline")

        orig = questions.requests.get
        try:
            questions.requests.get = fake_get
            data = questions.simple_http_request()
        finally:
            questions.requests.get = orig

        self.assertIsNone(data)


class TestSortedDict(unittest.TestCase):
    """
    8 Kata
    """
    def test_sorted_iteration(self):
        s = questions.SortedDict()
        s['banana'] = 'ccc'
        s['apple'] = 'aaa'
        s['orange'] = 'bbb'
        self.assertEqual(list(s.keys()), ['apple', 'banana', 'orange'])
        self.assertEqual(list(s.values()), ['aaa', 'ccc', 'bbb'])
        self.assertEqual(list(s.items()),
                         [('apple', 'aaa'), ('banana', 'ccc'), ('orange', 'bbb')])


class TestCacheList(unittest.TestCase):
    """
    8 Kata
    """
    def test_eviction(self):
        c = questions.CacheList(3)
        c.append(1)
        c.append(2)
        c.append(3)
        self.assertEqual(list(c), [1, 2, 3])
        c.append(1)
        self.assertEqual(list(c), [2, 3, 1])
        c.append(1)
        self.assertEqual(list(c), [3, 1, 1])

if __name__ == "__main__":
    import unittest
    unittest.main(verbosity=2)
