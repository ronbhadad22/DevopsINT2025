import os
import json
import tarfile
import socket
import sys
from datetime import datetime

# Toggle debug logs with env var. Default ON for local runs.
DEBUG = os.getenv("KATA_DEBUG", "1") == "1"


def dprint(msg: str) -> None:
    """Debug print to stderr if DEBUG is enabled."""
    if DEBUG:
        print(msg, file=sys.stderr)


def valid_parentheses(s):
    """
    3 Kata

    Validate that '()','{}','[]' are properly nested and ordered.
    """
    dprint(f"[DEBUG] valid_parentheses called with: {s}")
    pairs = {'(': ')', '{': '}', '[': ']'}
    stack = []
    for ch in s:
        dprint(f"[DEBUG] Processing char: {ch}, stack before: {stack}")
        if ch in pairs:
            stack.append(ch)
        elif ch in pairs.values():
            if not stack or pairs[stack.pop()] != ch:
                dprint("[DEBUG] Mismatch found. Returning False")
                return False
        else:
            dprint(f"[DEBUG] Invalid character found: {ch}")
            return False
    result = not stack
    dprint(f"[DEBUG] Result: {result}")
    return result


def fibonacci_fixme(n):
    """
    2 Kata

    Return the n-th Fibonacci number where F(1)=1, F(2)=1.
    Non-positive n -> 0.
    """
    dprint(f"[DEBUG] fibonacci_fixme called with: {n}")
    if n <= 0:
        return 0
    if n in (1, 2):
        return 1
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
        dprint(f"[DEBUG] a={a}, b={b}")
    return b


def most_frequent_name(file_path):
    """
    2 Kata

    Read names (one per line) and return the most frequent.
    If tie, return one of them. If file empty/missing -> None.
    """
    dprint(f"[DEBUG] most_frequent_name called with: {file_path}")
    if not os.path.exists(file_path):
        dprint("[DEBUG] File not found")
        return None
    freq = {}
    with open(file_path, 'r', encoding='utf-8') as fh:
        for line in fh:
            name = line.strip()
            if name:
                freq[name] = freq.get(name, 0) + 1
    dprint(f"[DEBUG] Frequency map: {freq}")
    if not freq:
        return None
    result = max(freq, key=freq.get)
    dprint(f"[DEBUG] Most frequent name: {result}")
    return result


def files_backup(dir_path):
    """
    3 Kata

    Create a tar.gz with all files under dir_path (recursive) named:
    'backup_<dir_name>_<yyyy-mm-dd>.tar.gz' in CWD.
    Return the archive file name (or None if dir missing).
    """
    dprint(f"[DEBUG] files_backup called with: {dir_path}")
    if not os.path.isdir(dir_path):
        dprint("[DEBUG] Directory not found")
        return None
    dir_name = os.path.basename(os.path.normpath(dir_path))
    date_str = datetime.now().strftime('%Y-%m-%d')
    archive_name = f"backup_{dir_name}_{date_str}.tar.gz"
    with tarfile.open(archive_name, 'w:gz') as tar:
        for root, _, files in os.walk(dir_path):
            for fn in files:
                full = os.path.join(root, fn)
                arcname = os.path.relpath(full, start=os.path.dirname(dir_path))
                dprint(f"[DEBUG] Adding file to archive: {full} as {arcname}")
                tar.add(full, arcname=arcname)
    dprint(f"[DEBUG] Created archive: {archive_name}")
    return archive_name


def replace_in_file(file_path, text, replace_text):
    """
    2 Kata

    Replace all occurrences of 'text' with 'replace_text' in-place.
    If path doesn't exist, do nothing (return None).
    """
    dprint(f"[DEBUG] replace_in_file called with: {file_path}, text='{text}', replace_text='{replace_text}'")
    if not os.path.exists(file_path):
        dprint("[DEBUG] File not found")
        return None
    with open(file_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    dprint(f"[DEBUG] Original content: {content}")
    content = content.replace(text, replace_text)
    with open(file_path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    dprint("[DEBUG] Updated content written")
    return None


def json_configs_merge(*json_paths):
    """
    2 Kata

    Merge multiple JSON files left-to-right; later files override earlier.
    Nonexistent files are skipped. Non-dict roots are ignored.
    """
    dprint(f"[DEBUG] json_configs_merge called with: {json_paths}")
    merged = {}
    for path in json_paths:
        if not os.path.exists(path):
            dprint(f"[DEBUG] Skipping missing file: {path}")
            continue
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        dprint(f"[DEBUG] Loaded data from {path}: {data}")
        if isinstance(data, dict):
            merged.update(data)
    dprint(f"[DEBUG] Merged result: {merged}")
    return merged


def monotonic_array(lst):
    """
    1 Kata

    True if list is monotonic non-decreasing or non-increasing.
    """
    dprint(f"[DEBUG] monotonic_array called with: {lst}")
    if len(lst) <= 2:
        return True
    non_dec = all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))
    non_inc = all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1))
    result = non_dec or non_inc
    dprint(f"[DEBUG] non_dec={non_dec}, non_inc={non_inc}, result={result}")
    return result


def matrix_avg(mat, rows=None):
    """
    2 Kata

    Average (integer) of a 3x3 matrix, optionally only specific rows.
    Returns 0 if 'rows' is [], or mat is empty.
    """
    dprint(f"[DEBUG] matrix_avg called with: mat={mat}, rows={rows}")
    if rows is None:
        values = [x for row in mat for x in row]
    else:
        values = [x for i, row in enumerate(mat) if i in rows for x in row]
    dprint(f"[DEBUG] Values considered: {values}")
    if not values:
        return 0
    result = sum(values) // len(values)
    dprint(f"[DEBUG] Average: {result}")
    return result


def merge_sorted_lists(l1, l2):
    """
    1 Kata

    Merge two sorted lists without using sort().
    """
    dprint(f"[DEBUG] merge_sorted_lists called with: {l1}, {l2}")
    i = j = 0
    out = []
    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            out.append(l1[i])
            i += 1
        else:
            out.append(l2[j])
            j += 1
    out.extend(l1[i:])
    out.extend(l2[j:])
    dprint(f"[DEBUG] Merged list: {out}")
    return out


def longest_common_substring(str1, str2):
    """
    4 Kata

    DP approach in O(n*m) time/space.
    """
    dprint(f"[DEBUG] longest_common_substring called with: '{str1}', '{str2}'")
    if not str1 or not str2:
        return ''
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    end_i = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_i = i
    result = str1[end_i - max_len:end_i]
    dprint(f"[DEBUG] Longest common substring: '{result}'")
    return result


def longest_common_prefix(str1, str2):
    """
    1 Kata

    Return the longest common prefix of two strings.
    """
    dprint(f"[DEBUG] longest_common_prefix called with: '{str1}', '{str2}'")
    limit = min(len(str1), len(str2))
    k = 0
    while k < limit and str1[k] == str2[k]:
        k += 1
    result = str1[:k]
    dprint(f"[DEBUG] Longest common prefix: '{result}'")
    return result


def rotate_matrix(mat):
    """
    2 Kata

    Rotate an n*m matrix clockwise.
    """
    dprint(f"[DEBUG] rotate_matrix called with: {mat}")
    if not mat:
        return []
    rows, cols = len(mat), len(mat[0])
    rotated = []
    for c in range(cols):
        new_row = []
        for r in range(rows - 1, -1, -1):
            new_row.append(mat[r][c])
        rotated.append(new_row)
    dprint(f"[DEBUG] Rotated matrix: {rotated}")
    return rotated


def is_valid_email(mail_str):
    """
    3 Kata

    Validate username@domain:
      - username starts with alnum; only [0-9a-zA-Z._]
      - domain must DNS-resolve.
    """
    dprint(f"[DEBUG] is_valid_email called with: {mail_str}")
    if not isinstance(mail_str, str) or '@' not in mail_str:
        return False
    user, _, domain = mail_str.partition('@')
    if not user or not domain:
        return False
    if not user[0].isalnum():
        return False
    if any(not (ch.isalnum() or ch in '._') for ch in user):
        return False
    try:
        socket.gethostbyname(domain)
    except Exception as e:
        dprint(f"[DEBUG] DNS resolution failed: {e}")
        return False
    return True


def pascal_triangle(lines):
    """
    3 Kata

    Print Pascal's triangle up to `lines`. Return None.
    (Numbers are printed to stdout; debug to stderr.)
    """
    dprint(f"[DEBUG] pascal_triangle called with: {lines}")
    if lines <= 0:
        return None
    row = [1]
    for _ in range(lines):
        # Keep outputs on stdout (tests capture this)
        print(' '.join(str(x) for x in row))
        nxt = [1]
        for i in range(1, len(row)):
            nxt.append(row[i - 1] + row[i])
        nxt.append(1)
        row = nxt
    return None


def list_flatten(lst):
    """
    2 Kata

    Flatten nested lists of arbitrary depth.
    """
    dprint(f"[DEBUG] list_flatten called with: {lst}")
    flat = []

    def _walk(item):
        if isinstance(item, list):
            for sub in item:
                _walk(sub)
        else:
            flat.append(item)

    _walk(lst)
    dprint(f"[DEBUG] Flattened list: {flat}")
    return flat


def str_compression(text):
    """
    2 Kata

    Compress consecutive runs: output list like [ch, count] but
    omit the count when it equals 1.
    """
    dprint(f"[DEBUG] str_compression called with: '{text}'")
    if not text:
        return []
    out = []
    cur = text[0]
    cnt = 1
    for ch in text[1:]:
        if ch == cur:
            cnt += 1
        else:
            out.append(cur)
            if cnt > 1:
                out.append(cnt)
            cur, cnt = ch, 1
    out.append(cur)
    if cnt > 1:
        out.append(cnt)
    dprint(f"[DEBUG] Compressed output: {out}")
    return out


def strong_pass(password):
    """
    1 Kata

    Strong if:
      - len >= 6
      - at least one digit, one lower, one upper, one special from !@#$%^&*()-+
    """
    dprint(f"[DEBUG] strong_pass called with: {password}")
    if not isinstance(password, str):
        return False
    if len(password) < 6:
        return False
    specials = set('!@#$%^&*()-+')
    has_d = any(ch.isdigit() for ch in password)
    has_l = any(ch.islower() for ch in password)
    has_u = any(ch.isupper() for ch in password)
    has_s = any(ch in specials for ch in password)
    result = has_d and has_l and has_u and has_s
    dprint(f"[DEBUG] has_d={has_d}, has_l={has_l}, has_u={has_u}, has_s={has_s}, result={result}")
    return result


# ---------------------- Smoke runner (kata_1-style prints) ----------------------
if __name__ == "__main__":
    def banner(name):
        print(f"\n{name}:\n--------------------")

    banner('valid_parentheses')
    print(valid_parentheses('[[{()}](){}]'))

    banner('fibonacci_fixme')
    print(fibonacci_fixme(6))

    banner('most_frequent_name')
    demo_names = "names_demo.txt"
    with open(demo_names, "w", encoding="utf-8") as f:
        f.write("alice\nbob\nalice\ncarol\n")
    print(most_frequent_name(demo_names))

    banner('files_backup')
    demo_dir = "files_to_backup"
    if os.path.isdir(demo_dir):
        print(files_backup(demo_dir))
    else:
        print(None)

    banner('replace_in_file')
    demo_yaml = "mnist-predictor.yaml"
    if not os.path.exists(demo_yaml):
        with open(demo_yaml, "w", encoding="utf-8") as f:
            f.write("image: {{IMG_NAME}}\n")
    print(replace_in_file(demo_yaml, "{{IMG_NAME}}", "mnist-pred:0.0.1"))

    banner('json_configs_merge')
    with open("default_demo.json", "w", encoding="utf-8") as f:
        f.write('{"a": 1, "b": 2}')
    with open("local_demo.json", "w", encoding="utf-8") as f:
        f.write('{"b": 3, "c": 4}')
    print(json_configs_merge("default_demo.json", "local_demo.json"))

    banner('monotonic_array')
    print(monotonic_array([1, 2, 3, 6, 8, 9, 0]))

    banner('matrix_avg')
    print(matrix_avg([[1, 2, 3], [4, 5, 6], [7, 8, 9]], rows=[0, 2]))
    print(matrix_avg([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    banner('merge_sorted_lists')
    print(merge_sorted_lists([1, 4, 9, 77, 13343], [-7, 0, 7, 23]))

    banner('longest_common_substring')
    print(longest_common_substring('abcdefg', 'bgtcdesd'))

    banner('longest_common_prefix')
    print(longest_common_prefix('abcd', 'ttty'))

    banner('rotate_matrix')
    print(rotate_matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))

    banner('is_valid_email')
    print(is_valid_email('israel.israeli@gmail.com'))

    banner('pascal_triangle')
    print(pascal_triangle(4))

    banner('list_flatten')
    print(list_flatten([1, 2, [3, 4, [4, 5], 7], 8]))

    banner('str_compression')
    print(str_compression('aaaabdddddhgf'))

    banner('strong_pass')
    print(strong_pass('##$FgC7^^5a'))
