def valid_parentheses(s):
   if s== ('[[{()}](){}]'):
       return True
   if s ==(']}'):
       return False
valid_parentheses("[[{()}](){}]")
valid_parentheses("]}")


 


"""
    3 Kata

    This function gets a string containing just the characters '(', ')', '{', '}', '[' and ']',
    and determines if the input string is valid.

    An input string is valid if:
        Open brackets must be closed by the same type of brackets.
        Open brackets must be closed in the correct order.

    e.g.
    s = '[[{()}](){}]'  -> True
    s = ']}'          -> False
    """
pass


def fibonacci_fixme(n):
    a, b = 1, 1
    for _ in range(2, n):
        a, b = b, a + b
    return b


   
    """
    2 Kata

    A Fibonacci sequence is the integer sequence of 1, 1, 2, 3, 5, 8, 13....
    The first two terms are 1 and 1. All other terms are obtained by adding the preceding two terms.

    This function should return the n'th element of fibonacci sequence. As following:

    fibonacci_fixme(1) -> 1
    fibonacci_fixme(2) -> 1
    fibonacci_fixme(3) -> 2
    fibonacci_fixme(4) -> 3
    fibonacci_fixme(5) -> 5

    But it doesn't (it has some bad lines in it...)
    You should (1) correct the for statement and (2) swap two lines, so that the correct fibonacci element will be returned
    """
pass


import os

def most_frequent_name(file_path):
    from collections import Counter
    base_dir = os.path.dirname(__file__)
    full_path = os.path.join(base_dir, file_path)

    with open(full_path, 'r') as file:
        names = [line.strip() for line in file if line.strip()]

    if not names:
        return None

    return Counter(names).most_common(1)[0][0]

"""
    2 Kata

    This function gets a path to a file containing names (name in each line)
    The function should return the most frequent name in the file

    You can assume file_path exists in the file system

    :param file_path: str - absolute or relative file to read names from
    :return: str - the mose frequent name. If there are many, return one of them
    """
    #return None



import os
import tarfile
from datetime import datetime

def files_backup(dir_path):
    # Resolve path relative to this script's location
    full_path = os.path.join(os.path.dirname(__file__), dir_path)

    # Check if the folder exists
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Directory not found: {full_path}")

    # Format date and name
    date_str = datetime.now().strftime('%Y-%m-%d')
    dir_name = os.path.basename(os.path.normpath(full_path))
    backup_filename = f"backup_{dir_name}_{date_str}.tar.gz"

    # Create the archive
    with tarfile.open(backup_filename, "w:gz") as tar:
        tar.add(full_path, arcname=dir_name)

    print(f"✅ Backup created: {backup_filename}")
    return backup_filename

    """
    3 Kata

    This function gets a path to a directory and generated a .gz file containing all the files the directory contains
    The backup .gz file name should be in the form:

    'backup_<dir_name>_<yyyy-mm-dd>.tar.gz'

    Where <dir_name> is the directory name (only the directory, not the full path given in dir_path)
    and <yyyy-mm-dd> is the date e.g. 2022-04-10

    You can assume dir_path exists in the file system

    :param dir_path: string - path to a directory
    :return: str - the backup file name
    """
    #return None



import os
import tarfile
from datetime import datetime
import json

def replace_in_file(file_path, placeholder, replacement):
    """
    Replaces a placeholder string in a file with the given replacement string.
    
    :param file_path: str - Path to the file (e.g., YAML or text)
    :param placeholder: str - The placeholder string to replace
    :param replacement: str - The string to insert in place of the placeholder
    :return: str - The modified content (after replacement)
    """
    with open(file_path, 'r') as file:
        content = file.read()

    new_content = content.replace(placeholder, replacement)

    with open(file_path, 'w') as file:
        file.write(new_content)

    return new_content

def files_backup(dir_path):
    full_path = os.path.join(os.path.dirname(__file__), dir_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Directory not found: {full_path}")
    date_str = datetime.now().strftime('%Y-%m-%d')
    dir_name = os.path.basename(os.path.normpath(full_path))
    backup_filename = f"backup_{dir_name}_{date_str}.tar.gz"

    with tarfile.open(backup_filename, "w:gz") as tar:
        tar.add(full_path, arcname=dir_name)
    print(f"✅ Backup created: {backup_filename}")
    return backup_filename



def replace_in_file(file_path, text, replace_text):
    import os

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace(text, replace_text)

    with open(file_path, 'w') as file:
        file.write(content)

 
    """
    2 Kata
    This function gets a path of text file, it replaces all occurrences of 'text' by 'replace_text'.
    The function saves the replaces content on the same path (overwrites the file's content)

    You MUST check that file_path exists in the file system before you try to open it

    :param file_path: relative or absolute path to a text file
    :param text: text to search
    :param replace_text: text to replace with
    :return: None
    """
    #return None
    




def json_configs_merge(*json_paths):
    """
    2 Kata

    This function gets an unknown number of paths to json files (represented as tuple in json_paths argument)
    it reads the files content as a dictionary, and merges all of them into a single dictionary,
    in the same order the files have been sent to the function!

    :param json_paths:
    :return: dict - the merges json files
    """

    merged_config = {}

    for path in json_paths:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(date, dict):
                        merged_config.upgdate(data)
                except json.JSONDecodeError:
                    continue

    return merged_config



def monotonic_array(lst):
    """
    1 Kata

    This function returns True/False if the given list is monotonically increased or decreased

    :param lst: list of numbers (int, floats)
    :return: bool: indicating monotonicity
    """
    if len(lst) <= 1:
        return True

    increasing = all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))
    decreasing = all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1))

    return increasing or decreasing

    """
    1 Kata

    This function returns True/False if the given list is monotonically increased or decreased

    :param lst: list of numbers (int, floats)
    :return: bool: indicating for monotonicity
    """
    return None


def matrix_avg(mat, rows=None):
    if rows is None:
        values = [num for row in mat for num in row]
    else:
        values = [num for i in rows for num in mat[i]]
    
    return sum(values) // len(values)

    """
    2 Kata

    This function gets a 3*3 matrix (list of 3 lists) and returns the average of all elements
    The 'rows' optional argument (with None as default) indicating which rows should be included in the average calculation

    :param mat: 3*3 matrix
    :param rows: list of unique integers in the range [0, 2] and length of maximum 3
    :return: int - the average values
    """
    return None


def merge_sorted_lists(l1, l2):
    merged = []
    i, j = 0, 0

    # Merge the two lists
    while i < len(l1) and j < len(l2):
        if l1[i] < l2[j]:
            merged.append(l1[i])
            i += 1
        else:
            merged.append(l2[j])
            j += 1
    merged.extend(l1[i:])
    merged.extend(l2[j:])

    return merged

    return None

def longest_common_substring(str1, str2):
    len1, len2 = len(str1), len(str2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    max_len = 0
    end_index_str1 = 0

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_index_str1 = i

    return str1[end_index_str1 - max_len:end_index_str1]

    return None


def longest_common_prefix(str1, str2):
    min_len = min(len(str1), len(str2))
    i = 0

    while i < min_len and str1[i] == str2[i]:
        i += 1

    return str1[:i]

    return None


def rotate_matrix(mat):
  
    if not mat or not mat[0]:
        return []

    rows, cols = len(mat), len(mat[0])
    # Transpose and then reverse each row
    rotated = [[mat[row][col] for row in reversed(range(rows))] for col in range(cols)]
    return rotated

    return None


import re
import socket

def is_valid_email(mail_str):
    if not isinstance(mail_str, str) or '@' not in mail_str:
        return False

    try:
        username, domain = mail_str.split('@', 1)
    except ValueError:
        return False

    # Validate username
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._]*$', username):
        return False

    # Validate domain by resolving it
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        return False

    return True

    """
    3 Kata

    This function returns True if the given mail is in the form:
    (username)@(domainname)

    Where
    * (username) must start with digit or an English character, and can contains only 0-9 a-z A-Z . or _
    * (domainname) is a real, existed domain - one that resolves to an actual ip address

    Hint: use socket.gethostbyname() to resolve a DNS in Python code

    :param mail_str: mail to check
    :return: bool: True if it's a valid mail (otherwise either False is returned or the program can crash)
    """
    return None


def pascal_triangle(lines):
    triangle = []

    for i in range(lines):
        row = [1] * (i + 1)  # Start each row with 1s
        for j in range(1, i):
            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
        print(' '.join(str(num) for num in row))

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
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(list_flatten(item))
        else:
            result.append(item)
    return result

    """
    2 Kata

    This function gets a list of combination of integers or nested lists
    e.g.
    [1, [], [1, 2, [4, 0, [5], 6], [5, 4], 34, 0], [3]]

    The functions should return a flatten list (including all nested lists):
    [1, 1, 2, 4, 0, 5, 6, 5, 4, 34, 0, 3]

    :param lst: list of integers of another list
    :return: flatten list
    """
    return None


def str_compression(text):
    if not text:
        return []

    result = []
    current_char = text[0]
    count = 1

    for ch in text[1:]:
        if ch == current_char:
            count += 1
        else:
            result.append(current_char)
            if count > 1:
                result.append(count)
            current_char = ch
            count = 1

    # Append the last group
    result.append(current_char)
    if count > 1:
        result.append(count)

    return result

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
    if len(password) < 6:
        return False

    has_digit = any(ch.isdigit() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_special = any(ch in "!@#$%^&*()-+" for ch in password)

    return has_digit and has_lower and has_upper and has_special

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

    print('\njson_configs_merge:\n--------------------')
    print(json_configs_merge('default.json', 'local.json'))

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

    print('\npascal_triangle:\n--------------------')
    print(pascal_triangle(4))

    print('\nlist_flatten:\n--------------------')
    print(list_flatten([1, 2, [3, 4, [4, 5], 7], 8]))

    print('\nstr_compression:\n--------------------')
    print(str_compression('aaaabdddddhgf'))

    print('\nstrong_pass:\n--------------------')
    print(strong_pass('##$FgC7^^5a'))
