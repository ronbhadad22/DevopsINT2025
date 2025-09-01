import os
import tarfile
import json
import socket
from datetime import date

def valid_parentheses(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack


def fibonacci_fixme(n):
    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b if n > 1 else 1


def most_frequent_name(file_path):
    with open(file_path) as f:
        names = f.read().splitlines()
    return max(set(names), key=names.count)


def files_backup(dir_path):
    name = os.path.basename(dir_path)
    fname = f"backup_{name}_{date.today()}.tar.gz"
    with tarfile.open(fname, "w:gz") as tar:
        tar.add(dir_path, arcname=name)
    return fname


def replace_in_file(file_path, text, replace_text):
    if not os.path.exists(file_path):
        return None
    with open(file_path) as f:
        content = f.read().replace(text, replace_text)
    with open(file_path, "w") as f:
        f.write(content)


def json_configs_merge(*paths):
    result = {}
    for p in paths:
        with open(p) as f:
            result.update(json.load(f))
    return result


def monotonic_array(lst):
    return lst == sorted(lst) or lst == sorted(lst, reverse=True)


def matrix_avg(mat, rows=None):
    if rows is None:
        rows = range(3)
    vals = [mat[r][c] for r in rows for c in range(3)]
    return sum(vals) // len(vals)


def merge_sorted_lists(l1, l2):
    res, i, j = [], 0, 0
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            res.append(l1[i]); i += 1
        else:
            res.append(l2[j]); j += 1
    return res + l1[i:] + l2[j:]


def longest_common_substring(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    longest, end = 0, 0
    for i in range(m):
        for j in range(n):
            if str1[i] == str2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
                if dp[i+1][j+1] > longest:
                    longest = dp[i+1][j+1]
                    end = i+1
    return str1[end-longest:end]


def longest_common_prefix(str1, str2):
    res = []
    for a, b in zip(str1, str2):
        if a == b:
            res.append(a)
        else:
            break
    return ''.join(res)


def rotate_matrix(mat):
    return [list(reversed(col)) for col in zip(*mat)]


def is_valid_email(mail_str):
    try:
        user, domain = mail_str.split('@')
        if not user or not domain:
            return False
        if not user[0].isalnum():
            return False
        if not all(c.isalnum() or c in "._" for c in user):
            return False
        socket.gethostbyname(domain)  # יזרוק שגיאה אם הדומיין לא קיים
        return True
    except:
        return False


def pascal_triangle(lines):
    tri = [[1]]
    for _ in range(1, lines):
        prev = tri[-1]
        tri.append([1] + [prev[i]+prev[i+1] for i in range(len(prev)-1)] + [1])
    for row in tri:
        print(" ".join(map(str, row)))


def list_flatten(lst):
    res = []
    for x in lst:
        if isinstance(x, list):
            res.extend(list_flatten(x))
        else:
            res.append(x)
    return res


def str_compression(text):
    if not text:
        return []
    res, count = [], 1
    for i in range(1, len(text)+1):
        if i < len(text) and text[i] == text[i-1]:
            count += 1
        else:
            res.append(text[i-1])
            if count > 1:
                res.append(count)
            count = 1
    return res


def strong_pass(password):
    if len(password) < 6:
        return False
    has_d = any(c.isdigit() for c in password)
    has_l = any(c.islower() for c in password)
    has_u = any(c.isupper() for c in password)
    has_s = any(c in "!@#$%^&*()-+" for c in password)
    return all([has_d, has_l, has_u, has_s])
