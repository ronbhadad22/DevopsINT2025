import unittest
from python_katas.kata_3 import questions

# -------------------- Knapsack --------------------
class TestKnapsack(unittest.TestCase):
    def test_knapsack(self):
        items = {
            'book': (3, 2),
            'television': (4, 3),
            'table': (6, 1),
            'scooter': (5, 4)
        }
        res = questions.knapsack(items, 8)
        self.assertIsInstance(res, set)
        # total value should be optimal
        total_value = sum(items[n][1] for n in res)
        self.assertEqual(total_value, 6)

# -------------------- TimeMe --------------------
class TestTimeMe(unittest.TestCase):
    def test_time_me(self):
        def dummy():
            sum(range(10))
        avg_time = questions.time_me(dummy)
        self.assertIsInstance(avg_time, float)
        self.assertGreaterEqual(avg_time, 0)

# -------------------- Tasks Scheduling --------------------
class TestTasksScheduling(unittest.TestCase):
    def test_tasks_scheduling(self):
        tasks = [(1,3), (2,5), (4,6), (6,8)]
        res = questions.tasks_scheduling(tasks)
        self.assertEqual(res, [0,2,3])

# -------------------- Valid DAG --------------------
class TestValidDAG(unittest.TestCase):
    def test_valid_dag_true(self):
        edges = [('a','b'), ('a','c'), ('b','d')]
        self.assertTrue(questions.valid_dag(edges))
    
    def test_valid_dag_false(self):
        edges = [('a','b'), ('b','a')]
        self.assertFalse(questions.valid_dag(edges))

# -------------------- Apache Logs Parser --------------------
class TestApacheLogsParser(unittest.TestCase):
    def test_apache_logs_parser(self):
        line = '[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico'
        parsed = questions.apache_logs_parser(line)
        self.assertEqual(parsed[1], "error")
        self.assertEqual(parsed[4], "72.15.99.187")

# -------------------- Simple HTTP Request --------------------
class TestSimpleHttpRequest(unittest.TestCase):
    def test_simple_http_request(self):
        import types
        def dummy_get(url):
            resp = types.SimpleNamespace()
            resp.raise_for_status = lambda : None
            resp.json = lambda : {"symbols": [1,2,3]}
            return resp
        import python_katas.kata_3.questions as q
        q.requests.get = dummy_get
        data = q.simple_http_request()
        self.assertIn("symbols", data)
        self.assertEqual(len(data["symbols"]), 3)

# -------------------- SortedDict --------------------
class TestSortedDict(unittest.TestCase):
    def test_sorteddict(self):
        d = questions.SortedDict()
        d["z"]=1; d["a"]=2; d["m"]=3
        self.assertEqual(d.keys(), ["a","m","z"])
        self.assertEqual(d.values(), [2,3,1])
        self.assertEqual(d.items(), [("a",2),("m",3),("z",1)])

# -------------------- CacheList --------------------
class TestCacheList(unittest.TestCase):
    def test_cachelist(self):
        cl = questions.CacheList(cache_size=3)
        cl.append(1); cl.append(2); cl.append(3); cl.append(4)
        self.assertEqual(cl, [2,3,4])
        cl.append(5)
        self.assertEqual(cl, [3,4,5])

# -------------------- YouTube Download (Skipped) --------------------
class TestYoutubeDownload(unittest.TestCase):
    @unittest.skip("Skipping YouTube download test in CI environment")
    def test_youtube_download(self):
        questions.youtube_download("dQw4w9WgXcQ")

# -------------------- Run All Tests --------------------
if __name__ == "__main__":
    unittest.main()
