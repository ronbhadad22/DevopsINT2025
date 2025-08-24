#q1
#כל סוגר פתוח נכנס ל־stack.
#כל סוגר סגור בודק את האחרון ב־stack.
#אם בסוף המחסנית ריקה → הסוגריים חוקיים.
#אם נשארו דברים או שיש אי־התאמה → לא חוקי.
def valid_parentheses(s):
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
    stack = []
    # מיפוי סוגר סגור לסוגר פתוח
    bracket_map = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in bracket_map.values():  # אם זה סוגר פתוח
            stack.append(char)
        elif char in bracket_map:        # אם זה סוגר סגור
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()
        else:
            # תווים אחרים לא אמורים להיות כאן
            return False

    # בסוף המחסנית חייבת להיות ריקה
    return len(stack) == 0


# דוגמאות:
print(valid_parentheses('[[{()}](){}]'))  # ➝ True
print(valid_parentheses(']}'))            # ➝ False


#q2
#האיבר הראשון והשני הם תמיד 1.
#כל איבר אחרי זה הוא סכום של שני האיברים הקודמים.
def fibonacci_fixme(n):
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
    if n == 1 or n == 2:
        return 1

    a, b = 1, 1
    for _ in range(3, n + 1):  # נכון: מתחילים מ-3 עד n
        a, b = b, a + b        # החלפה נכונה: a הופך להיות b, b הופך להיות a+b
    return b                   # מחזירים את האיבר האחרון (b)


# דוגמאות:
print(fibonacci_fixme(1))  # 1
print(fibonacci_fixme(2))  # 1
print(fibonacci_fixme(3))  # 2
print(fibonacci_fixme(4))  # 3
print(fibonacci_fixme(5))  # 5
print(fibonacci_fixme(10)) # 55

#q3
#with open(...) מבטיח שהקובץ ייסגר אוטומטית בסיום הקריאה.
#encoding='utf-8' מאפשר קריאה של טקסט בעברית או תווים מיוחדים.
#line.strip() מסיר רווחים או תווי newline בתחילת/סוף השורה.
#מחזירה את השם שמופיע הכי הרבה
from collections import Counter
import os

def most_frequent_name(file_name="names.txt"):
    """
    2 Kata

    This function gets a path to a file containing names (name in each line)
    The function should return the most frequent name in the file

    You can assume file_path exists in the file system

    :param file_path: str - absolute or relative file to read names from
    :return: str - the mose frequent name. If there are many, return one of them
    """
     # נתיב התיקייה של הסקריפט
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # נתיב מלא של הקובץ
    file_path = os.path.join(script_dir, file_name)

    # בדיקה שהקובץ קיים
    if not os.path.exists(file_path):
        print(f"Error: File '{file_name}' not found in script directory.")
        return None

    # קריאה וניתוח תוכן הקובץ
    with open(file_path, 'r', encoding='utf-8') as f:
        return Counter(line.strip() for line in f if line.strip()).most_common(1)[0][0]

# שימוש בפונקציה
if __name__ == "__main__":
    most_common_name = most_frequent_name()
    if most_common_name is not None:
        print(f"The most frequent name is: {most_common_name}")



#Q4
#הפונקציה מאפשרת לגבות תיקייה שלמה לתוך קובץ דחוס .tar.gz, עם שם קובץ שמכיל את שם התיקייה ואת התאריך של היום.
import os
import tarfile
from datetime import date  # או from datetime import datetime

def files_backup(dir_path):
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
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist.")
        return None

    dir_name = os.path.basename(dir_path.rstrip("/\\"))
    today = date.today().strftime("%Y-%m-%d")
    backup_file = f"backup_{dir_name}_{today}.tar.gz"

    try:
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(dir_path, arcname=dir_name)
        print(f"Backup successfully created: {backup_file}")
        return backup_file
    except PermissionError:
        print(f"Permission denied: Cannot create backup in this location.")
        return None
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

# נתיב התיקייה שברצונך לגבות
folder_to_backup = r"C:\Users\pnofa\OneDrive\שולחן העבודה\Python Project\DevopsINT2025\python_katas\kata_2"

# קריאה לפונקציה
backup_file = files_backup(folder_to_backup)




#Q5
#בודקת שהקובץ קיים-אם הקובץ לא נמצא בנתיב שציינת, הפונקציה לא ממשיכה ומדפיסה הודעת שגיאה.
#קוראת את כל תוכן הקובץ-למשתנה סטרינג
#מחליפה את הטקסט הרצוי
#שומרת את השינויים באותו הקובץ

def replace_in_file(file_path, text, replace_text):
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
    # בדיקה שהקובץ קיים
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # קריאה של תוכן הקובץ
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # החלפת הטקסט
    content = content.replace(text, replace_text)

    # שמירה חזרה לאותו הקובץ
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Replaced all occurrences of '{text}' with '{replace_text}' in '{file_path}'.")
    
#Q6
#הפונקציה הזו מבצעת מיזוג של כמה קבצי JSON לתוך מילון אחד (dictionary) בפייתון.
import json
import os

def json_configs_merge(*json_paths):
    """
    2 Kata

    This function gets an unknown number of paths to json files (represented as tuple in json_paths argument)
    it reads the files content as a dictionary, and merges all of them into a single dictionary,
    in the same order the files have been sent to the function!

    :param json_paths:
    :return: dict - the merges json files
    """
    # שמות הקבצים
    default_file = "default.json"
    local_file = "local.json"

    merged_dict = {}

    # בדיקה שהקבצים קיימים
    for file in [default_file, local_file]:
        if not os.path.exists(file):
            print(f"Error: File '{file}' does not exist.")
            return {}

    # קריאה ומיזוג הקבצים לפי סדר
    for file in [default_file, local_file]:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged_dict.update(data)

    return merged_dict

# שימוש בפונקציה
merged_data = ()
print("Merged JSON data:")
print(merged_data)

#Q7
#הפונקציה הזו בודקת אם רשימה של מספרים היא מונוטונית,
#מונוטונית עולה: כל איבר ברשימה קטן או שווה לאיבר הבא
#מונוטונית יורדת: כל איבר ברשימה גדול או שווה לאיבר הבא

def monotonic_array(lst):
    """
    1 Kata

    This function returns True/False if the given list is monotonically increased or decreased

    :param lst: list of numbers (int, floats)
    :return: bool: indicating for monotonicity
    """
    if len(lst) < 2:
        return True

    increasing = True
    decreasing = True

    for i in range(1, len(lst)):
        if lst[i] > lst[i-1]:
            decreasing = False
        if lst[i] < lst[i-1]:
            increasing = False

    return increasing or decreasing


# קריאות לבדיקה
print(monotonic_array([1, 2, 2, 3]))   # ✅ אמור להיות True
print(monotonic_array([5, 4, 4, 1]))   # ✅ אמור להיות True
print(monotonic_array([1, 3, 2]))      # ✅ אמור להיות False


#Q8
#חשב את הממוצע של כל האיברים במטריצה בגודל 3×3, או רק עבור שורות מסוימות אם המשתנה rows מוגדר.
def matrix_avg(mat, rows=None):
    """
    2 Kata

    This function gets a 3*3 matrix (list of 3 lists) and returns the average of all elements
    The 'rows' optional argument (with None as default) indicating which rows should be included in the average calculation

    :param mat: 3*3 matrix
    :param rows: list of unique integers in the range [0, 2] and length of maximum 3
    :return: int - the average values
    """
    if rows is None:
        rows_to_include = range(len(mat))
    else:
        rows_to_include = rows

    total = 0
    count = 0
    for r in rows_to_include:
        total += sum(mat[r])
        count += len(mat[r])

    if count == 0:
        return 0.0  # במקרה שאין שורות כלולות
    return total / count  # החזרה כ-float

# דוגמאות שימוש
mat = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix_avg(mat))        # ממוצע כל המטריצה -> 5.0
print(matrix_avg(mat, [0]))   # ממוצע שורה 0 -> 2.0
print(matrix_avg(mat, [1,2])) # ממוצע שורות 1 ו-2 -> 6.5

#q9
#למזג שתי רשימות ממוינות ביעילות בלי להשתמש ב־sort() או sorted(), אפשר להשתמש בשיטת two pointers.
def merge_sorted_lists(l1, l2):
    """
    1 Kata

    This function gets two sorted lists (each one of them is sorted)
    and returns a single sorted list combining both of them.

    Try to be as efficient as you can (hint - don't use Python's built in sort() or sorted() functions)

    :param l1: list of integers
    :param l2: list of integers
    :return: list: sorted list combining l1 and l2
    """
    i, j = 0, 0
    merged = []

    while i < len(l1) and j < len(l2):
        if l1[i] <= l2[j]:
            merged.append(l1[i])
            i += 1
        else:
            merged.append(l2[j])
            j += 1

    # אם נשארו איברים באחת הרשימות, מוסיפים אותם בסוף
    if i < len(l1):
        merged.extend(l1[i:])
    if j < len(l2):
        merged.extend(l2[j:])

    return merged

# דוגמאות שימוש
print(merge_sorted_lists([1,3,5], [2,4,6]))      # [1,2,3,4,5,6]
print(merge_sorted_lists([1,2,3], [4,5,6]))      # [1,2,3,4,5,6]
print(merge_sorted_lists([], [1,2,3]))           # [1,2,3]
print(merge_sorted_lists([1,2,3], []))           # [1,2,3]

#Q10
#מחזירה את תת-השרשרת הארוכה ביותר הזו.
def longest_common_substring(str1, str2):
    """
    4 Kata

    This functions gets two strings and returns their longest common substring

    e.g. for
    str1 = 'Introduced in 1991, The Linux kernel is an amazing software'
    str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'

    The returned value would be 'The Linux kernel is a'
    since it's the longest string contained both in str1 and str2

    :param str1: str
    :param str2: str
    :return: str - the longest common substring
    """
    m, n = len(str1), len(str2)
    # מטריצה לאחסון אורכי תתי השרשראות המשותפות
    dp = [[0] * (n+1) for _ in range(m+1)]
    max_len = 0
    end_pos = 0

    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
            else:
                dp[i][j] = 0

    return str1[end_pos - max_len:end_pos]
# דוגמה לשימוש
str1 = "Introduced in 1991, The Linux kernel is an amazing software"
str2 = "The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel."
print(longest_common_substring(str1, str2))
# Output: "The Linux kernel is a"

#q11

def longest_common_prefix(str1, str2):
    """
    1 Kata

    This functions gets two strings and returns their longest common prefix

    e.g. for
    str1 = 'The Linux kernel is an amazing software'
    str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'

    The returned value would be 'The Linux kernel is a'

    :param str1: str
    :param str2: str
    :return: str - the longest common prefix
    """
    min_length = min(len(str1), len(str2))
    prefix = ""

    for i in range(min_length):
        if str1[i] == str2[i]:
            prefix += str1[i]
        else:
            break

    return prefix

# דוגמה לשימוש
str1 = 'The Linux kernel is an amazing software'
str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'

print(longest_common_prefix(str1, str2))
# Output: 'The Linux kernel is a '

#Q12
#פונקציה שמקבלת מטריצה ומסובבת אותה 90 מעלות בכיוון השעון

def rotate_matrix(mat):
    """
    2 Kata

    This function gets a matrix n*m (list of m lists of length n) and rotate the matrix clockwise
    e.g.
    for [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]] which represent the matrix

    1   2   3
    4   5   6
    7   8   9
    10  11  12

    The output should be:
    [[10, 7, 4, 1], [11, 8, 5, 2], [12, 9, 6, 3]]

    10  7   4   1
    11  8   5   2
    12  9   6   3

    :param mat:
    :return: list of lists - rotate matrix
    """
    rows = len(mat)
    cols = len(mat[0]) if rows > 0 else 0

    # יצירת מטריצה חדשה ריקה בגודל cols*rows
    rotated = [[0] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            rotated[j][rows - 1 - i] = mat[i][j]

    return rotated

# דוגמה לשימוש
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
]

rotated_matrix = rotate_matrix(matrix)
print(rotated_matrix)
# Output: [[10, 7, 4, 1], [11, 8, 5, 2], [12, 9, 6, 3]]

#Q13
#פונקצייה שבודקת את תקינות המייל
import re
import socket
def is_valid_email(mail_str):
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
    pattern = r'^[a-zA-Z0-9][\w\.]*@([\w\-]+\.[\w\.-]+)$'
    match = re.match(pattern, mail_str)
    if not match:
        return False
    
    domain = match.group(1)
    
    try:
        # בדיקה אם הדומיין קיים
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

# דוגמאות
print(is_valid_email("test.user_1@gmail.com"))   # True (אם הדומיין קיים)
print(is_valid_email("1user@nonexistentdomain.xyz"))  # False
print(is_valid_email(".user@gmail.com"))  # False (username לא מתחיל עם אות או מספר)
print(is_valid_email("user@@gmail.com"))  # False

#Q14
#פונקציה שמדפיסה את משולש פסקל עד מספר השורות הנתון
#בונה רשימה של רשימות – כל שורה היא רשימה עם הערכים של משולש פסקל
#כל שורה מתחילה ומסתיימת ב־1.
#הערכים הפנימיים הם סכום שני הערכים שמעליהם בשורה הקודמת.


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
    triangle = []

    for i in range(lines):
        row = [1]  # השורה תמיד מתחילה ב-1
        if triangle:  # אם כבר יש שורות קודמות
            last_row = triangle[-1]
            # מחשב את הערכים שבין הקצוות
            row.extend([last_row[j] + last_row[j+1] for j in range(len(last_row)-1)])
            row.append(1)  # סוף השורה תמיד 1
        triangle.append(row)

    # הדפסת השורות
    for row in triangle:
        print(" ".join(map(str, row)))

# דוגמאות שימוש
pascal_triangle(10)

#Q15
#פונקציה שמקבלת רשימה (שיכולה לכלול מספרים וגם רשימות פנימיות), ומחזירה רשימה שטוחה (flattened) עם כל הערכים.
#אם האיבר הוא מספר → מוסיפים אותו ל־result.
#אם האיבר הוא רשימה → מפעילים את אותה פונקציה עליו (רקורסיה), ומוסיפים את התוצאה ל־result.
def list_flatten(lst):
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
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(list_flatten(item))  # קריאה רקורסיבית אם זה list
        else:
            result.append(item)
    return result


# דוגמת שימוש
example = [1, [], [1, 2, [4, 0, [5], 6], [5, 4], 34, 0], [3]]
print(list_flatten(example))
# פלט: [1, 1, 2, 4, 0, 5, 6, 5, 4, 34, 0, 3]

#Q16
#ונקציה שמבצעת דחיסה של טקסט ובכל פעם שסימן מופיע ברצף, היא מוסיפה אותו לרשימה + מספר פעמים שהוא הופיע (אם יותר מפעם אחת)פ
#אם הוא מופיע פעם אחת – אפשר להוסיף רק את התו בלי מספר
#
#
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
     # אם הטקסט ריק – נחזיר רשימה ריקה
    if not text:
        return []

    result = []   # כאן נאחסן את התוצאה
    count = 1     # מונה להופעות רצופות של אותו תו

    # נרוץ על כל התווים במחרוזת
    for i in range(1, len(text) + 1):
        if i < len(text) and text[i] == text[i - 1]:
            # אם התו הנוכחי זהה לקודם – נגדיל מונה
            count += 1
        else:
            # מוסיפים את התו לרשימה
            result.append(text[i - 1])
            # אם הוא הופיע יותר מפעם אחת – מוסיפים גם את המספר
            if count > 1:
                result.append(count)
            # מאפסים את המונה
            count = 1

    return result


# דוגמה
text = 'aaaaabbcaasbbgvccf'
print(str_compression(text))


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
    # 1) בדיקת אורך
    if len(password) < 6:
        return False

    # 2) דגלים לבדיקת תנאים
    has_digit = False
    has_lower = False
    has_upper = False
    has_special = False

    special_chars = set("!@#$%^&*()-+")

    # מעבר על כל תו בסיסמה
    for ch in password:
        if ch.isdigit():
            has_digit = True
        elif ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch in special_chars:
            has_special = True

    # החזרת תוצאה – True רק אם כל התנאים מתקיימים
    return has_digit and has_lower and has_upper and has_special

print(strong_pass("Aa1!aa"))   # True
print(strong_pass("aaaaaa"))   # False (אין ספרה, אות גדולה ותו מיוחד)
print(strong_pass("A1!"))      # False (קצר מדי)
print(strong_pass("Abcdef1"))  # False (אין תו מיוחד)

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
