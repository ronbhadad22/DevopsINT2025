

def valid_parentheses(s):
    prev = None
    while prev != s:  
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""



def fibonacci_fixme(n):

    if not isinstance(n, int):
        raise TypeError("Input must be an integer")

    if n <= 0:
        raise ValueError("Input must be a positive integer")

    if n == 1 or n == 2:
        return 1

    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


from collections import Counter

def most_frequent_name(file_path):
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, "r") as file:
        names = [line.strip() for line in file if line.strip()]

    if not names:
        raise ValueError("File is empty or contains no valid names")

    name_counts = Counter(names)
    return name_counts.most_common(1)[0][0]







import os
import tarfile
from datetime import date

def files_backup(dir_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, dir_path)
    dir_name = os.path.basename(os.path.normpath(dir_path))
    today_str = date.today().strftime("%Y-%m-%d")
    backup_filename = f"backup_{dir_name}_{today_str}.tar.gz"

    with tarfile.open(backup_filename, "w:gz") as tar:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=dir_path)
                tar.add(file_path, arcname=arcname)

    return backup_filename







def replace_in_file(file_path, text, replace_text):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"The file does not exist.\nLooked for: {abs_path}")
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = content.replace(text, replace_text)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(new_content)




def json_configs_merge(*json_paths):
    """
    2 Kata

    This function gets an unknown number of paths to json files (represented as tuple in json_paths argument)
    it reads the files content as a dictionary, and merges all of them into a single dictionary,
    in the same order the files have been sent to the function!

    :param json_paths:
    :return: dict - the merges json files
    """
    return None


def monotonic_array(lst):
    if len(lst) < 2:
        return True

    increasing = decreasing = True

    for i in range(1, len(lst)):
        if lst[i] > lst[i-1]:
            decreasing = False
        elif lst[i] < lst[i-1]:
            increasing = False
        if not increasing and not decreasing:
            return False

    return True


def matrix_avg(mat, rows=None):
    if rows is None:
        rows = [0, 1, 2]
    total = 0
    count = 0
    for r in rows:
        for value in mat[r]:
            total += value
            count += 1
    return total / count


def merge_sorted_lists(l1, l2):
    result = []
    i, j = 0, 0
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            result.append(l1[i])
            i += 1
        else:
            result.append(l2[j])
            j += 1
    result.extend(l1[i:])
    result.extend(l2[j:])
    return result



def longest_common_substring(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    max_len = 0
    end_idx = 0  

    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_idx = i
            else:
                dp[i][j] = 0

    return str1[end_idx - max_len:end_idx]


def longest_common_prefix(str1, str2):
    min_len = min(len(str1), len(str2))
    i = 0
    while i < min_len and str1[i] == str2[i]:
        i += 1
    return str1[:i]



def rotate_matrix(mat):
    if not mat:
        return []
    n = len(mat)
    m = len(mat[0])
    rotated = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            rotated[i][j] = mat[n - 1 - j][i]
    return rotated



import re
import socket

def is_valid_email(mail_str):
    if '@' not in mail_str:
        return False
    username, domain = mail_str.split('@', 1)
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._]*$', username):
        return False
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        return False
    return True



def pascal_triangle(lines):
    """
    3 Kata

    This function gets an integer representing the number of lines to print in a Pascal Triangle
    e.g. For n = 10 then following would be printed

                 1
                1 1
               1 2 1
              1 3 3 1
             1 4 6 4 1
           1 5 10 10 5 1
         1 6 15 20 15 6 1
        1 7 21 35 35 21 7 1
      1 8 28 56 70 56 28 8 1
    1 9 36 84 126 126 84 36 9 1

    You are allowed to print the numbers not in a triangle shape:
    1
    1 1
    1 2 1
    1 3 3 1
    1 4 6 4 1
    1 5 10 10 5 1
    1 6 15 20 15 6 1
    1 7 21 35 35 21 7 1
    1 8 28 56 70 56 28 8 1
    1 9 36 84 126 126 84 36 9 1

    :param lines: int
    :return: None
    """
    return None


def list_flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(list_flatten(item))
        else:
            flat_list.append(item)
    return flat_list



def str_compression(text):
    """
    2 Kata

    This function gets a text (string) and returns a list representing the compressed form of the text.
    e.g.
    text = 'aaaaabbcaasbbgvccf'

    The output will be:
    ['a', 5, 'b', 2, 'c', 'a', 2, 's', 1, 'b', 2, 'g', 'v', 'c', 2, 'f']

    Since 'a' appears 5 times in consecutively, 'b' 2 times etc...
    Note that sequences of length 1 don't necessarily have the number 1 after the character (like 'c' before 'a')

    :param text: str
    :return: list representing the compressed form of the string
    """
    return None


def strong_pass(password):
    """
    1 Kata

    A password is considered strong if it satisfies the following criteria:
    1) Its length is at least 6.
    2) It contains at least one digit.
    3) It contains at least one lowercase English character.
    4) It contains at least one uppercase English character.
    5) It contains at least one special character. The special characters are: !@#$%^&*()-+

    This function returns True if the given password is strong enough
    """
    return None


if __name__ == '__main__':
    print('\nvalid_parentheses:\n--------------------')
    print(valid_parentheses('[[{()}](){}]'))

    print('\nfibonacci_fixme:\n--------------------')
    print(fibonacci_fixme(6))

    print('\nmost_frequent_name:\n--------------------')
    print(most_frequent_name('names.txt'))

    print('\nfiles_backup:\n--------------------')
    print(files_backup('files_to_backup'))

    print('\nreplace_in_file:\n--------------------')
    print(replace_in_file('mnist-predictor.yaml', '{{IMG_NAME}}', 'mnist-pred:0.0.1'))

    # print('\njson_configs_merge:\n--------------------')
    # print(json_configs_merge('default.json', 'local.json'))

    print('\nmonotonic_array:\n--------------------')
    print(monotonic_array([1, 2, 3, 6, 8, 9, 0]))

    print('\nmatrix_avg:\n--------------------')
    print(matrix_avg([[1, 2, 3], [4, 5, 6], [7, 8, 9]], rows=[0, 2]))
    print(matrix_avg([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    print('\nmerge_sorted_lists:\n--------------------')
    print(merge_sorted_lists([1, 4, 9, 77, 13343], [-7, 0, 7, 23]))

    print('\nlongest_common_substring:\n--------------------')
    print(longest_common_substring('abcdefg', 'bgtcdesd'))

    print('\nlongest_common_prefix:\n--------------------')
    print(longest_common_prefix('abcd', 'ttty'))

    print('\nrotate_matrix:\n--------------------')
    print(rotate_matrix([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]))

    print('\nis_valid_email:\n--------------------')
    print(is_valid_email('israel.israeli@gmail.com'))

    # print('\npascal_triangle:\n--------------------')
    # print(pascal_triangle(4))

    print('\nlist_flatten:\n--------------------')
    print(list_flatten([1, 2, [3, 4, [4, 5], 7], 8]))

    # print('\nstr_compression:\n--------------------')
    # print(str_compression('aaaabdddddhgf'))

    # print('\nstrong_pass:\n--------------------')
    # print(strong_pass('##$FgC7^^5a'))
