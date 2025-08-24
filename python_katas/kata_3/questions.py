
#import requests  # to be used in simple_http_request()

ISO_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

#Q1
#פונקציה מחשבת איזה פריטים לבחור כך שהשק לא יהיה כבד מדי אבל הערך הכולל יהיה הכי גבוה שאפשר.
#items – מילון שבו המפתח הוא שם הפריט, והערך הוא זוג ((משקל, ערך)).
#יוצרים טבלה דו־ממדית dp בגודל: (מספר פריטים + 1) × (קיבולת השק + 1).
#הערך המקסימלי שאפשר לקבל אם מסתכלים רק על i פריטים ראשונים ובקיבולת שק w.

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
    # שמירת הפריטים עם אינדקס
    names = list(items.keys())
    weights = [items[name][0] for name in names]
    values = [items[name][1] for name in names]
    n = len(items)

    # טבלת DP: שורות = פריטים, עמודות = קיבולת
    dp = [[0] * (knapsack_limit + 1) for _ in range(n + 1)]

    # מילוי הטבלה
    for i in range(1, n + 1):
        for w in range(1, knapsack_limit + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # שיחזור הפריטים שנבחרו
    chosen = set()
    w = knapsack_limit
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # המשמעות: הפריט נבחר
            chosen.add(names[i - 1])
            w -= weights[i - 1]

    return chosen
items = {
    "bed": (100, 15),
    "iphone13": (1, 1500),
    "tv": (20, 300),
    "painting": (2, 1000)
}

print(knapsack(items, 50))

#Q2
#מטרה כאן היא לכתוב פונקציה שמודדת את זמן הריצה הממוצע של פונקציה אחרת
#לקבל פונקצייה=>להריץ 100 פעמים=>למדוד זמן ריצה=>להחזיר ממוצע של זמן ריצה
import time
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
    total_time = 0.0
    
    for _ in range(runs):
        start = time.perf_counter()   # זמן מדויק במיוחד
        func()
        end = time.perf_counter()
        total_time += (end - start)
    
    return total_time / runs
def test_func():
    sum([i for i in range(10000)])

print(time_me(test_func))


#Q3
def youtube_download(video_id):
    """
    3 Kata

    Youtube video url is in the form https://www.youtube.com/watch?v=<video id>
    This function get a youtube video id and downloads this video to the local fs

    hint: https://www.bogotobogo.com/VideoStreaming/YouTube/youtube-dl-embedding.php

    :param video_id: str
    :return: None
    """
    

#Q4
#לבחור את מספר המשימות המרבי שניתן לבצע מבלי שהן יתחפפו בזמנים.
#המטרה: לבחור את הקבוצה הגדולה ביותר של משימות שאינן חופפות.
#קודם כל ממיינים את כל המשימות לפי זמן הסיום שלהן מהקטן לגדול.
#מתחילים עם משימה שהסתיימה הכי מוקדם (או הראשונה במיון).
#אחרי שבחרנו משימה, מעבירים את "הזמן האחרון" לנקודת הסיום שלה.
#enumerate(tasks) נותן לנו (index, task), כדי שנוכל להחזיר את האינדקסים בסוף.
#x[1][1] הוא זמן הסיום של המשימה.

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
    # שמירת האינדקס המקורי
    indexed_tasks = list(enumerate(tasks))
    
    # מיון לפי זמן סיום
    indexed_tasks.sort(key=lambda x: x[1][1])  # x[1][1] = end time
    
    selected_indexes = []
    last_end_time = None
    
    for idx, (start, end) in indexed_tasks:
        if last_end_time is None or start >= last_end_time:
            selected_indexes.append(idx)
            last_end_time = end
    
    return selected_indexes

from datetime import datetime

tasks = [
    (datetime(2025, 8, 24, 9), datetime(2025, 8, 24, 12)),
    (datetime(2025, 8, 24, 10), datetime(2025, 8, 24, 11)),
    (datetime(2025, 8, 24, 13), datetime(2025, 8, 24, 15)),
]

print(tasks_scheduling(tasks))  # יכול להחזיר [1, 2] או [0, 2] בהתאם למיון


#Q5

def valid_dag(edges):
    from collections import defaultdict
    """
    5 Kata

    Given a DAG (https://en.wikipedia.org/wiki/Directed_acyclic_graph) in the form:
    [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]

    where a, b, c, d, e are vertices and ('a', 'b') etc... are edges
    This function determine whether the graph is a valid DAG

    :param edges: list of tuples of string 'a', 'b'....
    :return: bool - True if and only if it is a valid DAG
    """

    # בונים מילון של צמתים עם רשימת שכנים
    graph = defaultdict(list)
    nodes = set()
    for u, v in edges:
        graph[u].append(v)
        nodes.add(u)
        nodes.add(v)

    visited = set()
    rec_stack = set()

    def dfs(node):
        if node in rec_stack:  # מעגל
            return True
        if node in visited:    # כבר ביקרנו ואין מעגל
            return False

        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if dfs(neighbor):
                return True

        rec_stack.remove(node)
        return False

    for node in nodes:
        if dfs(node):  # אם נמצא מעגל
            return False

    return True  # אם לא נמצא אף מעגל → זה DAG
edges1 = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), 
          ('b', 'd'), ('c', 'd'), ('c', 'e')]

edges2 = [('a', 'b'), ('b', 'c'), ('c', 'a')]  # מכיל מעגל

print(valid_dag(edges1))  # True – אין מעגל, זה DAG
print(valid_dag(edges2))  # False – יש מעגל (a → b → c → a)


#Q6
from utils import open_img, save_img
import os

def rotate_img(img_filename):
    """
    3 Kata

    Rotates image clockwise

    :param img_filename: image file path (png or jpeg)
    :return: None, the rotated image should be saved as 'rotated_<original image filename>'
    """
     # פותחים את התמונה למטריצה
    image = open_img(img_filename)

    # סיבוב מטריצה 90 מעלות בכיוון השעון
    rotated_img = [list(row) for row in zip(*image[::-1])]

    # שם הקובץ החדש
    base_name = os.path.basename(img_filename)
    new_filename = f'rotated_{base_name}'

    # שמירת התמונה החדשה
    save_img(rotated_img, new_filename)

    print(f"Image saved as {new_filename}")

# דוגמה לקריאה לפונקציה
# רק צריך לשים את שם הקובץ של התמונה באותה תיקייה
rotate_img(r"C:\Users\pnofa\OneDrive\שולחן העבודה\Python Project\DevopsINT2025\python_katas\kata_3\67203.jpeg")

#Q7
import os
from utils import open_img, save_img

def matrix_avg(mat):
    rows = len(mat)
    cols = len(mat[0])
    new_mat = [[0]*cols for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            neighbors = []
            for x in range(max(0,i-1), min(rows,i+2)):
                for y in range(max(0,j-1), min(cols,j+2)):
                    neighbors.append(mat[x][y])
            new_mat[i][j] = sum(neighbors)/len(neighbors)
    return new_mat

def img_blur(img_filename):
    """
    4 Kata

    Blurs an image (every pixel is an average of its nearest neighbors)

    :param img_filename: image file path (png or jpeg)
    :return: None, the rotated image should be saved as 'rotated_<original image filename>'
    """
    # פותחים את התמונה למטריצה
    image = open_img(img_filename)

    # מטשטשים את התמונה
    blured_img = matrix_avg(image)

    # שמירת הקובץ החדש
    base_name = os.path.basename(img_filename)
    new_filename = f'blured_{base_name}'
    save_img(blured_img, new_filename)
    print(f"Image saved as {new_filename}")

# דוגמה לקריאה לפונקציה
img_blur(r"C:\Users\pnofa\OneDrive\שולחן העבודה\Python Project\DevopsINT2025\python_katas\kata_3\67203.jpeg")

#Q8
#לקחת שורה אחת מתוך לוג של Apache ולחלק אותה לשדות מובנים, כך שניתן יהיה לעבוד איתה בתוכנה בקלות.
import re
from datetime import datetime

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
    date, level, pid, tid, client_ip, log = ..., ..., ..., ..., ..., ...
    # regex pattern לפי פורמט הלוג
    pattern = r'\[(.*?)\] \[(.*?):(.*?)\] \[pid (\d+):tid (\d+)\] \[client (.*?)\] (.*)'

    match = re.match(pattern, apache_single_log)
    if not match:
        raise ValueError("Log format not recognized")

    # חיתוך השדות
    date_str, module, level, pid, tid, client_ip, log_msg = match.groups()

    # המרה של date למועד datetime
    date = datetime.strptime(date_str, "%a %b %d %H:%M:%S.%f %Y")

    # המרה של pid ו‑tid ל־int
    pid = int(pid)
    tid = int(tid)

    return date, level, pid, tid, client_ip, log_msg
log_line = "[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico"

parsed = apache_logs_parser(log_line)
print(parsed)

#Q9
#פונקציה הזו המטרה היא לבצע בקשה פשוטה ל־Binance API ולקבל מידע על שוק ההחלפות (market exchange info).
#משתמשים ב־requests כדי לשלוח בקשה HTTP.
#לאחר קבלת התגובה, משתמשים ב־.json() כדי להמיר את התגובה לאובייקט Python (dict/list).
import requests 
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
    data = response.json()
    return data

# שימוש בפונקציה
market_data = simple_http_request()
print(market_data)

#Q10
#מחלקה בשם SortedDict שתתנהג כמו מילון רגיל (dict), אבל תסדר את המפתחות שלה לפי סדר אלפביתי או סדר גודל (לפי סוג המפתחות) בכל פעם שמסתכלים עליהם.
#גדרת מילון רגיל – זה מחלקה שיורשת מ־dict.
#סידור המפתחות – בכל קריאה ל־keys(), values() או items() צריך להחזיר את הערכים לפי סדר המפתחות.
#הוספת פריטים – כל פעם שמוסיפים פריט חדש (__setitem__) המפתח צריך להיכלל בסדר המיון.
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def keys(self):
        return sorted(super().keys())

    def values(self):
        return [self[k] for k in self.keys()]

    def items(self):
        return [(k, self[k]) for k in self.keys()]
x = SortedDict()
x['banana'] = 'ccc'
x['apple'] = 'aaa'
x['orange'] = 'bbb'

print(list(x.keys()))    # ['apple', 'banana', 'orange']
print(list(x.values()))  # ['aaa', 'ccc', 'bbb']
print(list(x.items()))   # [('apple', 'aaa'), ('banana', 'ccc'), ('orange', 'bbb')]



#Q11
#הרשימה שומרת תמיד את ה־n האיברים האחרונים בלבד:
#הרשימה מתנהגת כמו רשימה רגילה (list) אבל שומרת רק את מספר האיברים שהוגדר ב־cache_size.
#super() מאפשר לנו לגשת למתודות של המחלקה ההורה (list במקרה שלנו) מתוך המחלקה הנוכחית (CacheList).
#pop() היא מתודת רשימות בפייתון שמסירה ומחזירה איבר מהתא האחרון ברשימה או ממיקום מסוים אם מציינים אינדקס.
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
        self.cache_size = cache_size

    def append(self, element):
        super().append(element)
        # אם הרשימה ארוכה מדי, מסירים את הפריטים הישנים ביותר
        while len(self) > self.cache_size:
            self.pop(0)
x = CacheList(3)

x.append(1)
x.append(2)
x.append(3)
print(x)  # [1, 2, 3]

x.append(1)
print(x)  # [2, 3, 1]

x.append(1)
print(x)  # [3, 1, 1]

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
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T13:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T11:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T16:00:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T14:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T14:05:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T12:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T13:30:00Z', ISO_FORMAT)),
        (datetime.strptime('2022-01-01T10:00:00Z', ISO_FORMAT), datetime.strptime('2022-01-01T10:10:00Z', ISO_FORMAT))
    ])
    print(tasks)

    print('\nvalid_dag\n--------------------')

    # valid
    print(valid_dag([('a', 'b'), ('a', 'c'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))

    # invalid
    print(valid_dag([('a', 'b'), ('c', 'a'), ('a', 'd'), ('a', 'e'), ('b', 'd'), ('c', 'd'), ('c', 'e')]))

    print('\nrotate_img\n--------------------')
    rotate_img('67203.jpeg')

    print('\nimg_blur\n--------------------')
    img_blur('67203.jpeg')

    print('\napache_logs_parser\n--------------------')
    date, level, pid, tid, client_ip, log = apache_logs_parser('[Fri Sep 09 10:42:29.902022 2011] [core:error] [pid 35708:tid 4328636416] [client 72.15.99.187] File does not exist: /usr/local/apache2/htdocs/favicon.ico')
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
