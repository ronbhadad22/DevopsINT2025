def sum_of_element(elements):
    """
    1 Kata
    :param elements: list of integers
    :return: Return int - the sum of all elements.
    """
    total = 0
    for moshe in elements:
        print(moshe)
        total += moshe
    return total


def verbing(word):
    """
    1 Kata
    Given a string 'word', if its length is at least 3, add 'ing' to its end.
    Unless it already ends in 'ing', in which case add 'ly' instead.
    If the string length is less than 3, leave it unchanged.
    """
    if len(word) < 3:
        return word
    if word.endswith('ing'):
        return word + 'ly'
    return word + 'ing'


def words_concatenation(words):
    """
    1 Kata
    Given a list of words, concatenates them with spaces.
    """
    return ' '.join(words)


def reverse_words_concatenation(words):
    """
    1 Kata
    Given a list of words, concatenates them in reverse order with spaces.
    """
    return ' '.join(reversed(words))


def is_unique_string(some_str):
    """
    2 Kata
    True if all characters are unique, else False.
    """
    return len(set(some_str)) == len(some_str)


def list_diff(elements):
    """
    1 Kata
    Return a diff list: first element None; each next is current - previous.
    """
    if not elements:
        return []
    result = [None]
    for i in range(1, len(elements)):
        result.append(elements[i] - elements[i - 1])
    return result


def prime_number(num):
    """
    1 Kata
    Check if the given number is prime.
    """
    if num < 2:
        return False
    i = 2
    while i * i <= num:
        if num % i == 0:
            return False
        i += 1
    return True


def palindrome_num(num):
    """
    1 Kata
    Check whether a number is palindrome.
    """
    s = str(num)
    return s == s[::-1]


def pair_match(men, women):
    """
    3 Kata
    Return (man_name, woman_name) with minimal absolute age diff.
    If either dict is empty, return None.
    """
    if not men or not women:
        return None
    min_diff = float('inf')
    best = None
    for m_name, m_age in men.items():
        for w_name, w_age in women.items():
            diff = abs(m_age - w_age)
            if diff < min_diff:
                min_diff = diff
                best = (m_name, w_name)
    return best


def bad_average(a, b, c):
    """
    1 Kata
    FIXED: average of three numbers.
    """
    return (a + b + c) / 3


def best_student(grades):
    """
    1 Kata
    Return key (student) with highest grade; None if empty.
    """
    if not grades:
        return None
    return max(grades, key=grades.get)


def print_dict_as_table(some_dict):
    """
    1 Kata
    Print dict as:
    Key     Value
    -------------
    <k>     <v>
    """
    print("Key\tValue")
    print("-------------")
    for k, v in some_dict.items():
        print(f"{k}\t{v}")


def merge_dicts(dict1, dict2):
    """
    1 Kata
    Merge dict2 into dict1 and return dict1.
    """
    dict1.update(dict2)
    return dict1


def seven_boom(n):
    """
    1 Kata
    Return list of numbers 1..n that are 'boom' (multiple of 7 or contain '7').
    """
    if n <= 0:
        return []
    res = []
    for i in range(1, n + 1):
        if i % 7 == 0 or '7' in str(i):
            res.append(i)
    return res


def caesar_cipher(str_to_encrypt):
    """
    2 Kata
    Caesar cipher shift 3 (A-Z, a-z), keep non-letters unchanged.
    """
    out = []
    for ch in str_to_encrypt:
        if 'a' <= ch <= 'z':
            out.append(chr(((ord(ch) - 97 + 3) % 26) + 97))
        elif 'A' <= ch <= 'Z':
            out.append(chr(((ord(ch) - 65 + 3) % 26) + 65))
        else:
            out.append(ch)
    return ''.join(out)


def sum_of_digits(digits_str):
    """
    1 Kata
    Sum digits in a numeric string; '' -> 0
    """
    if not digits_str:
        return 0
    return sum(int(ch) for ch in digits_str)
