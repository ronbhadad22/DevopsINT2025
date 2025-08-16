import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from python_katas.kata_3 import kata_questions_3 as questions
from python_katas.utils import unittest_runner

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class TestKnapsack(unittest.TestCase):
    """5 Kata"""
    def test_sample(self):
        items = {
            'book': (3, 2),
            'television': (4, 3),
            'table': (6, 1),
            'scooter': (5, 4)
        }
        chosen = questions.knapsack(items, knapsack_limit=8)
        self.assertEqual(set(chosen), {'scooter', 'book'})

class TestTimeMe(unittest.TestCase):
    """2 Kata"""
    def test_returns_mean_seconds(self):
        def noop():
            return None
        avg = questions.time_me(noop)
        self.assertIsInstance(avg, float)
        self.assertGreaterEqual(avg, 0.0)

class TestYoutubeDownload(unittest.TestCase):
    """3 Kata"""
    @patch("builtins.print")  # quiet logs
    def test_does_not_crash_without_yt_dlp(self, _):
        # Should not raise even if yt_dlp isn't installed.
        questions.youtube_download("VIDEOID123")

class TestTasksScheduling(unittest.TestCase):
    """5 Kata"""
    def test_activity_selection(self):
        tasks = [
            (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),  # 0
            (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),  # 1
            (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),  # 2
            (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),  # 3
            (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),  # 4
            (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT)),  # 5
        ]
        chosen = questions.tasks_scheduling(tasks)

        # Must match the known optimal solution
        self.assertEqual(chosen, [5, 4, 3])

        # Additional robustness: ensure non-overlap
        for i in range(len(chosen) - 1):
            a_end = tasks[chosen[i]][1]
            b_start = tasks[chosen[i+1]][0]
            self.assertLessEqual(a_end, b_start)

        # And ensure we can’t do better than len(chosen)
        # (quick check by brute force for such a tiny input)
        import itertools
        def ok(sub):
            sub_sorted = sorted(sub, key=lambda idx: tasks[idx][1])
            for i in range(len(sub_sorted)-1):
                if tasks[sub_sorted[i]][1] > tasks[sub_sorted[i+1]][0]:
                    return False
            return True
        best = 0
        for r in range(1, len(tasks)+1):
            for comb in itertools.combinations(range(len(tasks)), r):
                if ok(comb):
                    best = max(best, len(comb))
        self.assertEqual(len(chosen), best)

class TestValidDag(unittest.TestCase):
    """5 Kata"""
    def test_valid_and_invalid(self):
        self.assertTrue(questions.valid_dag(
            [('a','b'),('a','c'),('a','d'),('a','e'),('b','d'),('c','d'),('c','e')]
        ))
        self.assertFalse(questions.valid_dag(
            [('a','b'),('c','a'),('a','c')]  # simple cycle a->c->a
        ))

class TestRotateImg(unittest.TestCase):
    """3 Kata"""
    @patch("python_katas.kata_3.kata_questions_3.open_img", return_value=[[1,2,3],[4,5,6]])
    @patch("python_katas.kata_3.kata_questions_3.save_img")
    def test_rotate(self, mock_save, mock_open):
        questions.rotate_img("sample.jpeg")
        # Rotated of [[1,2,3],[4,5,6]] is [[4,1],[5,2],[6,3]]
        expected = [[4,1],[5,2],[6,3]]
        saved = mock_save.call_args[0][0]
        self.assertEqual(saved, expected)
        self.assertIn("rotated_", mock_save.call_args[0][1])

class TestImgBlur(unittest.TestCase):
    """4 Kata"""
    @patch("python_katas.kata_3.kata_questions_3.open_img", return_value=[
        [1,2,3],
        [4,5,6],
        [7,8,9],
    ])
    @patch("python_katas.kata_3.kata_questions_3.save_img")
    def test_blur(self, mock_save, mock_open):
        questions.img_blur("x.png")
        saved = mock_save.call_args[0][0]
        # Center (1,1) should be average of all neighbors+itself:
        self.assertEqual(saved[1][1], sum(range(1,10))//9)
        self.assertIn("blured_", mock_save.call_args[0][1])

class TestApacheLogsParser(unittest.TestCase):
    """3 Kata"""
    def test_sample(self):
        s = "[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico"
        date, level, pid, tid, ip, msg = questions.apache_logs_parser(s)
        self.assertEqual(level, "error")
        self.assertEqual(pid, 35708)
        self.assertEqual(tid, 4328636416)
        self.assertEqual(ip, "72.15.99.187")
        self.assertIn("favicon.ico", msg)
        self.assertEqual(date.year, 2011)

class TestSimpleHttpRequest(unittest.TestCase):
    """2 Kata"""
    @patch("python_katas.kata_3.kata_questions_3.requests.get")
    def test_ok(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"serverTime": 123, "symbols": []}
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = questions.simple_http_request()
        self.assertIn("serverTime", data)
        self.assertIn("symbols", data)

    @patch("python_katas.kata_3.kata_questions_3.requests.get", side_effect=Exception("offline"))
    def test_failure_returns_empty_dict(self, _):
        data = questions.simple_http_request()
        self.assertEqual(data, {})

class TestSortedDict(unittest.TestCase):
    """8 Kata"""
    def test_sorted_behavior(self):
        s = questions.SortedDict()
        s['banana'] = 'ccc'
        s['apple'] = 'aaa'
        s['orange'] = 'bbb'
        self.assertEqual(list(s.keys()), ['apple', 'banana', 'orange'])
        self.assertEqual(list(s.values()), ['aaa', 'ccc', 'bbb'])
        self.assertEqual(list(s.items()), [('apple', 'aaa'), ('banana', 'ccc'), ('orange', 'bbb')])

class TestCacheList(unittest.TestCase):
    """8 Kata"""
    def test_cache_eviction(self):
        c = questions.CacheList(3)
        c.append(1); c.append(2); c.append(3)
        self.assertEqual(list(c), [1,2,3])
        c.append(1)  # evicts oldest (1)
        self.assertEqual(list(c), [2,3,1])
        c.append(1)  # evicts 2
        self.assertEqual(list(c), [3,1,1])

if __name__ == '__main__':
    import inspect, sys
    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))
