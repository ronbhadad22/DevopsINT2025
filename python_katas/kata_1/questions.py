def sum_of_element(elements):
    """
    1 Kata
    :param elements: list of integers
    :return: Return int - the sum of all elements.
    """
    total = 0
    for e in elements:
        total += e
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
    elif word.endswith('ing'):
        return word + 'ly'
    else:
        return word + 'ing'


def words_concatenation(words):
    """
    1 Kata
    Given a list of words, return them concatenated with spaces.
    """
    return ' '.join(words)


def reverse_words_concatenation(words):
    """
    1 Kata
    Concatenate words in reverse order.
    """
    return ' '.join(words[::-1])


def is_unique_string(some_str):
    """
    2 Kata
    Return True if all characters are unique, False otherwise.
    """
    return len(set(some_str)) == len(some_str)


def list_diff(elements):
    """
    1 Kata
    Return diff list: each element is reduced by its previous one.
    First element should be None.
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
    Check if number is prime.
    """
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def palindrome_num(num):
    """
    1 Kata
    Check if number is palindrome.
    """
    return str(num) == str(num)[::-1]


def pair_match(men, women):
    """
    3 Kata
    Find (man, woman) pair with minimal age difference.
    """
    min_diff = float("inf")
    best_pair = None
    for m_name, m_age in men.items():
        for w_name, w_age in women.items():
            diff = abs(m_age - w_age)
            if diff < min_diff:
                min_diff = diff
                best_pair = (m_name, w_name)
    return best_pair


def bad_average(a, b, c):
    """
    1 Kata
    Fix average calculation.
    """
    return (a + b + c) / 3


def best_student(grades):
    """
    1 Kata
    Return student with highest grade.
    """
    return max(grades, key=grades.get)


def print_dict_as_table(some_dict):
    """
    1 Kata
    Print dictionary in table format.
    """
    print("Key     Value")
    print("-------------")
    for key, value in some_dict.items():
        print(f"{key:<7} {value}")


def merge_dicts(dict1, dict2):
    """
    1 Kata
    Merge dict2 into dict1 and return it.
    """
    dict1.update(dict2)
    return dict1


def seven_boom(n):
    """
    1 Kata
    Return list of all 7-booms from 1..n
    """
    result = []
    for i in range(1, n + 1):
        if i % 7 == 0 or '7' in str(i):
            result.append(i)
    return result


def caesar_cipher(str_to_encrypt):
    """
    2 Kata
    Caesar cipher with shift=3.
    """
    result = ""
    for char in str_to_encrypt:
        if char == " ":
            result += " "
        elif char.isalpha():
            shift = 3
            if char.islower():
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
    return result


def sum_of_digits(digits_str):
    """
    1 Kata
    Sum digits in a string.
    """
    total = 0
    for digit in digits_str:
        total += int(digit)
    return total


if __name__ == '__main__':

    print('\nsum_of_element:\n--------------------')
    print(sum_of_element([1, 2]))
    print(sum_of_element([1, 3]))
    print(sum_of_element([4, 5, 6]))

    print('\nverbing:\n--------------------')
    print(verbing('walk'))
    print(verbing('swimming'))
    print(verbing('do'))

    print('\nwords_concatenation:\n--------------------')
    print(words_concatenation(['take', 'me', 'home']))

    print('\nreverse_words_concatenation:\n--------------------')
    print(reverse_words_concatenation(['take', 'me', 'home']))

    print('\nis_unique_string:\n--------------------')
    print(is_unique_string('aasdssdsederd'))
    print(is_unique_string('12345tgbnh'))

    print('\nlist_diff:\n--------------------')
    print(list_diff([1, 2, 3, 8, 77, 0]))

    print('\nprime_number:\n--------------------')
    print(prime_number(5))
    print(prime_number(22))

    print('\npalindrome_num:\n--------------------')
    print(palindrome_num(12221))
    print(palindrome_num(577))

    print('\npair_match:\n--------------------')
    print(pair_match(
        {"John": 20, "Abraham": 45},
        {"July": 18, "Kim": 26}
    ))

    print('\nbad_average:\n--------------------')
    print(bad_average(1, 2, 3))

    print('\nbest_student:\n--------------------')
    print(best_student({
        "Ben": 78,
        "Hen": 88,
        "Natan": 99,
        "Efraim": 65,
        "Rachel": 95
    }))

    print('\nprint_dict_as_table:\n--------------------')
    print_dict_as_table({
        "Ben": 78,
        "Hen": 88,
        "Natan": 99,
        "Efraim": 65,
        "Rachel": 95
    })

    print('\nmerge_dicts:\n--------------------')
    print(merge_dicts({'a': 1}, {'b': 2}))

    print('\nseven_boom:\n--------------------')
    print(seven_boom(30))

    print('\ncaesar_cipher:\n--------------------')
    print(caesar_cipher('Fly Me To The Moon'))

    print('\nsum_of_digits:\n--------------------')
    print(sum_of_digits('1223432'))
