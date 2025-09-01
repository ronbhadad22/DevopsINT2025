def sum_of_element(elements):
    return sum(elements)


def verbing(word):
    if len(word) < 3:
        return word
    if word.endswith('ing'):
        return word + 'ly'
    return word + 'ing'


def words_concatenation(words):
    return ' '.join(words) 


def reverse_words_concatenation(words):
    return ' '.join(words[::-1])


def is_unique_string(some_str):
    return len(set(some_str)) == len(some_str)


def list_diff(elements):
    if not elements:
        return []
    diff = [None]
    for i in range(1, len(elements)):
        diff.append(elements[i] - elements[i-1])
    return diff


def prime_number(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def palindrome_num(num):
    s = str(num)
    return s == s[::-1]


def pair_match(men, women):
    min_diff = float('inf')
    best_pair = (None, None)
    for m_name, m_age in men.items():
        for w_name, w_age in women.items():
            diff = abs(m_age - w_age)
            if diff < min_diff:
                min_diff = diff
                best_pair = (m_name, w_name)
    return best_pair


def bad_average(a, b, c):
  
    return (a + b + c) / 3


def best_student(grades):
    return max(grades, key=grades.get)


def print_dict_as_table(some_dict):
    print('Key     Value')
    print('-------------')
    for k, v in some_dict.items():
        print(f'{k:<7} {v}')


def merge_dicts(dict1, dict2):
    dict1.update(dict2)
    return dict1


def seven_boom(n):
    result = []
    for i in range(1, n+1):
        if i % 7 == 0 or '7' in str(i):
            result.append(i)
    return result


def caesar_cipher(str_to_encrypt):
    result = ''
    for c in str_to_encrypt:
        if 'a' <= c <= 'z':
            result += chr(((ord(c) - ord('a') + 3) % 26) + ord('a'))
        elif 'A' <= c <= 'Z':
            result += chr(((ord(c) - ord('A') + 3) % 26) + ord('A'))
        else:
            result += c
    return result


def sum_of_digits(digits_str):
    return sum(int(d) for d in digits_str) if digits_str else 0

