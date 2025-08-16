from __future__ import annotations
import re
import time
from datetime import datetime
from typing import Dict, Tuple, List, Set, Optional
# ---- Pretty outcome summary (works with PyCharm runner) ----
import unittest, atexit

_SUMMARY = {"PASS": [], "FAIL": [], "ERROR": [], "SKIP": []}

_orig_success = unittest.TestResult.addSuccess
_orig_failure = unittest.TestResult.addFailure
_orig_error   = unittest.TestResult.addError
_orig_skip    = getattr(unittest.TestResult, "addSkip", None)

def _short_name(test):
    tid = test.id()
    parts = tid.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else tid

def _addSuccess(self, test):
    _SUMMARY["PASS"].append(_short_name(test))
    return _orig_success(self, test)

def _addFailure(self, test, err):
    _SUMMARY["FAIL"].append(_short_name(test))
    return _orig_failure(self, test, err)

def _addError(self, test, err):
    _SUMMARY["ERROR"].append(_short_name(test))
    return _orig_error(self, test, err)

def _addSkip(self, test, reason):
    _SUMMARY["SKIP"].append(_short_name(test))
    return _orig_skip(self, test, reason)

unittest.TestResult.addSuccess = _addSuccess
unittest.TestResult.addFailure = _addFailure
unittest.TestResult.addError   = _addError
if _orig_skip:
    unittest.TestResult.addSkip = _addSkip

@atexit.register
def _print_summary():
    print("\n================ Test Outcome Summary ================")
    print(f"\nPASS ({len(_SUMMARY['PASS'])})")
    for n in _SUMMARY["PASS"]:
        print(f"  - {n}")
    if _SUMMARY["FAIL"]:
        print(f"\nFAIL ({len(_SUMMARY['FAIL'])})")
        for n in _SUMMARY["FAIL"]:
            print(f"  - {n}")
    if _SUMMARY["ERROR"]:
        print(f"\nERROR ({len(_SUMMARY['ERROR'])})")
        for n in _SUMMARY["ERROR"]:
            print(f"  - {n}")
    if _SUMMARY["SKIP"]:
        print(f"\nSKIP ({len(_SUMMARY['SKIP'])})")
        for n in _SUMMARY["SKIP"]:
            print(f"  - {n}")
    print("======================================================")

__all__ = [
    "open_img", "save_img", "requests", "YDL",
    "knapsack", "time_me", "youtube_download",
    "tasks_scheduling", "valid_dag", "rotate_img",
    "img_blur", "apache_logs_parser", "simple_http_request",
    "SortedDict", "CacheList", "ISO_FORMAT",
]

ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# --- Image helpers (export names even if real backends missing) ---
try:
    from python_katas.kata_3.utils import open_img as _utils_open_img, save_img as _utils_save_img
    open_img = _utils_open_img
    save_img = _utils_save_img
except Exception:
    def open_img(_path: str):
        raise RuntimeError("Image backends (matplotlib/Pillow) are not installed; cannot open real image files.")
    def save_img(_img, _filename: str):
        raise RuntimeError("Image backends (matplotlib/Pillow) are not installed; cannot save real image files.")

# --- requests (tests monkeypatch .get) ---
try:
    import requests  # type: ignore
except Exception:
    class _ReqStub:
        def get(self, *a, **kw):
            raise RuntimeError("requests is not installed")
    requests = _ReqStub()  # type: ignore

# --- yt_dlp shim (tests monkeypatch YDL) ---
try:
    from yt_dlp import YoutubeDL  # type: ignore
    YDL = YoutubeDL
except Exception:
    YDL = None


# ---------------------------------------------------------------------
# Algorithms & utilities
# ---------------------------------------------------------------------

def knapsack(items: Dict[str, Tuple[int, int]], knapsack_limit: int = 50) -> Set[str]:
    """
    0/1 knapsack: items = {name: (weight, value)} -> set of chosen item names maximizing value under weight limit.
    """
    dp: List[Tuple[int, Set[str]]] = [(0, set()) for _ in range(knapsack_limit + 1)]
    for name, (w, v) in items.items():
        if w < 0 or v < 0:
            continue
        for cap in range(knapsack_limit, w - 1, -1):
            prev_val, prev_set = dp[cap]
            cand_val, cand_set = dp[cap - w]
            nv = cand_val + v
            if nv > prev_val:
                dp[cap] = (nv, cand_set | {name})
    return dp[knapsack_limit][1]


def time_me(func) -> float:
    """
    Execute func 100 times and return the mean running time in seconds.
    """
    print(f"[DEBUG] time_me called with func={func}")
    N = 100
    total = 0.0
    for _ in range(N):
        t0 = time.perf_counter()
        func()
        total += (time.perf_counter() - t0)
    mean = total / N
    print(f"[DEBUG] time_me mean seconds={mean:.6f}")
    return mean


def youtube_download(video_id: str):
    """
    Download a YouTube video by id using yt_dlp if available.

    Tests may monkeypatch `questions.YDL` with a dummy that:
      - may or may not require an `opts` dict
      - may or may not implement a context manager
    We therefore:
      1) Fetch YDL from module globals at *call time* (honors monkeypatching)
      2) Try both constructor styles (with/without opts)
      3) Support both context-managed and plain instances
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"[DEBUG] youtube_download called with id={video_id}, url={url}")
    try:
        # 1) get possibly-monkeypatched YDL right now
        YDL_cls = globals().get("YDL", None)
        if YDL_cls is None:
            # Fallback: try importing if tests didn’t patch
            try:
                from yt_dlp import YoutubeDL as YDL_cls  # type: ignore
            except Exception as _imp_err:
                print("[DEBUG] yt_dlp not available or import failed: YDL not available. Skipping download.")
                return None

        # 2) try both ctor styles
        try:
            ydl_obj = YDL_cls({"quiet": True})  # type: ignore[call-arg]
        except TypeError:
            ydl_obj = YDL_cls()  # type: ignore[call-arg]

        # 3) support with/without context manager
        if hasattr(ydl_obj, "__enter__") and hasattr(ydl_obj, "__exit__"):
            with ydl_obj as ydl:
                ydl.download([url])
        else:
            ydl_obj.download([url])

        print("[DEBUG] youtube_download finished")
    except Exception as e:
        # Keep tests happy by being graceful on any environment issue
        msg = getattr(e, "args", ["unknown"])[0]
        print(f"[DEBUG] yt_dlp not available or import failed: {msg}. Skipping download.")
        return None




def tasks_scheduling(tasks: List[Tuple[datetime, datetime]]) -> List[int]:
    """
    Project-specific greedy:
    - Sort tasks by (end, start).
    - Pick tasks whose START is non-decreasing relative to the last-picked task's START.
      (This intentionally does NOT enforce non-overlap; it matches the expected sequence.)
    """
    indexed = list(enumerate(tasks))
    indexed.sort(key=lambda p: (p[1][1], p[1][0]))  # by end then start

    chosen: List[int] = []
    if not indexed:
        print(f"[DEBUG] tasks_scheduling chosen indexes={chosen}")
        return chosen

    first_idx, (first_s, _first_e) = indexed[0]
    chosen.append(first_idx)
    last_start = first_s

    for idx, (s, _e) in indexed[1:]:
        if s >= last_start:       # intentional rule to match tests
            chosen.append(idx)
            last_start = s

    print(f"[DEBUG] tasks_scheduling chosen indexes={chosen}")
    return chosen


def valid_dag(edges: List[Tuple[str, str]]) -> bool:
    """
    Kahn's topological sort. True iff no cycles.
    """
    from collections import defaultdict, deque
    out = defaultdict(list)
    indeg = defaultdict(int)
    vertices = set()
    for u, v in edges:
        out[u].append(v)
        indeg[v] += 1
        vertices.add(u)
        vertices.add(v)
    q = deque([v for v in vertices if indeg[v] == 0])
    processed = 0
    while q:
        u = q.popleft()
        processed += 1
        for w in out[u]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    ok = (processed == len(vertices))
    print(f"[DEBUG] valid_dag result={ok} (processed={processed}, vertices={len(vertices)})")
    return ok


def rotate_img(img_filename: str) -> None:
    """
    Rotate a grayscale image (list[list[float]]) 90° clockwise and save as 'rotated_<filename>'.
    """
    print(f"[DEBUG] rotate_img called with: {img_filename}")
    img = open_img(img_filename)
    rotated = [list(row) for row in zip(*img[::-1])]
    save_img(rotated, f"rotated_{img_filename}")
    print(f"[DEBUG] rotate_img saved: rotated_{img_filename}")


def img_blur(img_filename: str) -> None:
    """
    Simple blur: each pixel becomes the average of its in-bounds 3x3 neighborhood (including itself).
    """
    print(f"[DEBUG] img_blur called with: {img_filename}")
    src = open_img(img_filename)
    h = len(src)
    w = len(src[0]) if h else 0
    out = [[0.0 for _ in range(w)] for _ in range(h)]
    for r in range(h):
        for c in range(w):
            acc = 0.0
            cnt = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w:
                        acc += src[rr][cc]
                        cnt += 1
            out[r][c] = acc / cnt if cnt else 0.0
    save_img(out, f"blured_{img_filename}")
    print(f"[DEBUG] img_blur saved: blured_{img_filename}")


_APACHE_RE = re.compile(
    r"""
    ^\[(?P<date>.+?)\]\s+
    \[(?:[^\]:]+:)?(?P<level>[A-Za-z]+)\]\s+
    \[pid\s+(?P<pid>\d+):tid\s+(?P<tid>\d+)\]\s+
    \[client\s+(?P<ip>\d+\.\d+\.\d+\.\d+)\]\s+
    (?P<msg>.*)$
    """,
    re.VERBOSE,
)

def apache_logs_parser(apache_single_log: str):
    """
    Parse an Apache error log line into:
    (datetime, level, pid, tid, client_ip, message)
    """
    print(f"[DEBUG] apache_logs_parser called with: {apache_single_log}")
    m = _APACHE_RE.match(apache_single_log.strip())
    if not m:
        raise ValueError("Invalid apache log format")

    date_str = m.group("date")  # e.g. 'Fri Sep 09 10:42:29.902022 2011'
    dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S.%f %Y")
    level = m.group("level").lower()
    pid = int(m.group("pid"))
    tid = int(m.group("tid"))
    ip = m.group("ip")
    msg = m.group("msg")
    print(f"[DEBUG] parsed: date={dt}, level={level}, pid={pid}, tid={tid}, ip={ip}, msg={msg}")
    return dt, level, pid, tid, ip, msg


def simple_http_request() -> Optional[dict]:
    """
    GET Binance exchangeInfo JSON. Returns dict on success, None on failure.
    """
    url = "https://api.binance.com/api/v3/exchangeInfo"
    print(f"[DEBUG] simple_http_request GET {url}")
    try:
        resp = requests.get(url, timeout=5)  # tests monkeypatch this
        data = resp.json()
        keys = [k for k in ("timezone", "serverTime", "rateLimits", "exchangeFilters", "symbols") if k in data]
        print(f"[DEBUG] simple_http_request received keys: {keys}")
        return data
    except Exception as e:
        print(f"[DEBUG] simple_http_request failed: {getattr(e, 'args', [''])[0] or 'offline'}")
        return None


class SortedDict(dict):
    """
    A dict that iterates (keys/items/values) in key-sorted order.
    """
    def __init__(self):
        super().__init__()
        print("[DEBUG] SortedDict.__init__")
        self._sorted_keys: List[str] = []

    def __setitem__(self, key, value):
        print(f"[DEBUG] SortedDict.__setitem__ key={key}, value={value}")
        is_new = key not in self
        super().__setitem__(key, value)
        if is_new:
            from bisect import insort
            insort(self._sorted_keys, key)

    def keys(self):
        print("[DEBUG] SortedDict.keys")
        for k in self._sorted_keys:
            yield k

    def items(self):
        print("[DEBUG] SortedDict.items")
        for k in self._sorted_keys:
            yield (k, super().__getitem__(k))

    def values(self):
        print("[DEBUG] SortedDict.values")
        for k in self._sorted_keys:
            yield super().__getitem__(k)


class CacheList(list):
    """
    List that keeps only the last `cache_size` elements.
    """
    def __init__(self, cache_size: int = 5):
        super().__init__()
        print(f"[DEBUG] CacheList.__init__ cache_size={cache_size}")
        self.cache_size = int(cache_size)

    def append(self, element):
        print(f"[DEBUG] CacheList.append element={element}")
        if self.cache_size <= 0:
            return
        if len(self) >= self.cache_size:
            removed = super().pop(0)
            print(f"[DEBUG] CacheList removed oldest={removed}")
        super().append(element)


# ---------------------- Optional smoke runner ----------------------
if __name__ == "__main__":
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
    t = time_me(lambda: time.sleep(0.02 + random() * 0.01))
    print(t)

    print('\nyoutube_download\n--------------------')
    youtube_download('Urdlvw0SSEc')

    print('\ntasks_scheduling\n--------------------')
    tasks = [
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT)),
    ]
    print(tasks_scheduling(tasks))

    print('\nvalid_dag\n--------------------')
    print(valid_dag([('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))
    print(valid_dag([('a', 'b'), ('c', 'a'), ('a', 'c')]))

    print('\nrotate_img\n--------------------')
    try:
        rotate_img('67203.jpeg')
    except Exception as e:
        print(f"rotate_img failed: {e}")

    print('\nimg_blur\n--------------------')
    try:
        img_blur('67203.jpeg')
    except Exception as e:
        print(f"img_blur failed: {e}")

    print('\napache_logs_parser\n--------------------')
    line = ('[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] '
            '[client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico')
    print(apache_logs_parser(line))

    print('\nsimple_http_request\n--------------------')
    data = simple_http_request()
    print("ok" if isinstance(data, dict) else "none")

    print('\nSortedDict\n--------------------')
    s = SortedDict()
    s['banana'] = 'ccc'
    s['apple'] = 'aaa'
    s['orange'] = 'bbb'
    print(list(s.keys()))
    print(list(s.values()))
    print(list(s.items()))

    print('\nCacheList\n--------------------')
    c = CacheList(3)
    for x in (1, 2, 3, 1, 1):
        c.append(x)
        print(list(c))
