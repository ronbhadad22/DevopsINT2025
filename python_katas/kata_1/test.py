import unittest
from python_katas.kata_1 import questions
from python_katas.utils import unittest_runner

testers = ['Ofir', 'Rima', 'Beny']


class TestSumOfElements(unittest.TestCase):
    """
    1 Katas
    """

    def sum_of_element(elements):
        return sum(elements)

    def test_empty_list(self):
        lst = []
        self.assertEqual(questions.sum_of_element(lst), 0)

    def test_integers_list(self):
        lst = [1, 2, 3, 4, 5]
        self.assertEqual(questions.sum_of_element(lst), 15)

    def test_negative_numbers(self):
        lst = [1, -6, 7, 0, 99]
        self.assertEqual(questions.sum_of_element(lst), 101)

    def test_all_zeros(self):
        lst = [0] * 50000
        self.assertEqual(questions.sum_of_element(lst), 0)


class TestVerbing(unittest.TestCase):
    """
    1 Katas
    """

    def test_string_longer_than_3_not_include_ing(self):
        word = 'teach'
        self.assertEqual(questions.verbing(word), 'teaching')

    def test_string_longer_than_3_include_ing(self):
        word = 'teaching'
        new_word = questions.verbing(word)
        self.assertTrue('ly' in new_word)

    def test_string_shorter_than_3(self):
        word = 'Hi'
        self.assertEqual(questions.verbing(word), word)

    def test_string_empty(self):
        word = ''
        self.assertEqual(questions.verbing(word), '')


class TestWordsConcatenation(unittest.TestCase):
    """
    1 Katas
    """

    def test_non_empty_strings_concatenation(self):
        string_list = ["app", "ban", "date"]
        self.assertEqual(questions.words_concatenation(string_list), "app ban date")

    def test_empty_and_non_empty_string_concatenation(self):
        string_list = ["app", "", "ban"]
        self.assertEqual(questions.words_concatenation(string_list), "app ban")

    def test_empty_list(self):
        string_list = []
        self.assertEqual(questions.words_concatenation(string_list), "")

    def test_non_empty_and_string_with_spaces(self):
        string_list = ["app", "     ", "ban"]
        self.assertEqual(questions.words_concatenation(string_list), "app       ban")


class TestReverseWordsConcatenation(unittest.TestCase):
    """
    1 Katas
    """

    def test_reverse_word_concatenation_with_for_non_empty_strings(self):
        string_list = ["app", "ban", "date"]
        self.assertEqual(questions.reverse_words_concatenation(string_list), "date ban app")

    def test_reverse_word_concatenation_with_empty_string_in_the_middle(self):
        string_list = ["app", "", "date"]
        self.assertEqual(questions.reverse_words_concatenation(string_list), "date app")

    def test_reverse_word_concatenation_with_empty_string_at_the_start(self):
        string_list = ["", "ban", "date"]
        self.assertEqual(questions.reverse_words_concatenation(string_list), "date ban")

    def test_reverse_word_concatenation_with_empty_string_at_the_end(self):
        string_list = ["app", "ban", ""]
        self.assertEqual(questions.reverse_words_concatenation(string_list), "ban app")

    def test_reverse_word_concatenation_with_different_len_strings(self):
        string_list = ["application", "banana", "sky"]
        self.assertEqual(questions.reverse_words_concatenation(string_list), "sky banana application")


class TestIsUniqueString(unittest.TestCase):
    """
    2 Katas
    """

    def test_only_unique_chars(self):
        word = 'abcdef'
        self.assertEqual(questions.is_unique_string(word), True)

    def test_not_unique_chars(self):
        word = 'aaabcdef'
        self.assertEqual(questions.is_unique_string(word), False)

    def test_empty_string(self):
        word = ''
        self.assertEqual(questions.is_unique_string(word), True)

    def test_spaces_string(self):
        word = '    '
        self.assertEqual(questions.is_unique_string(word), False)


class TestListDiff(unittest.TestCase):
    """
    1 Katas
    """

    def test_list_diff(self):
        elements = [1, 2, 3, 4, 7, 11]
        expected = [None, 1, 1, 1, 3, 4]
        self.assertEqual(questions.list_diff(elements), expected)

    def test_list_diff_2(self):
        elements_2 = [1, 5, 0, 4, 1, 1, 1]
        expected_2 = [None, 4, -5, 4, -3, 0, 0]
        self.assertEqual(questions.list_diff(elements_2), expected_2)

    def test_empty_list_diff(self):
        elements = []
        expected = []
        self.assertEqual(questions.list_diff(elements), expected)

    def test_one_element_list_diff(self):
        elements = [1]
        expected = [None]
        self.assertEqual(questions.list_diff(elements), expected)


class TestPrimeNumber(unittest.TestCase):
    """
    1 Katas
    """

    def test_primeNumber(self):
        num_to_check = 102
        self.assertEqual(questions.prime_number(num_to_check), False)

    def test_primeNumber_2(self):
        num_to_check = 97
        self.assertEqual(questions.prime_number(num_to_check), True)

    def test_primeNumber_3(self):
        num_to_check = 87
        self.assertEqual(questions.prime_number(num_to_check), False)

    def test_primeNumber_4(self):
        num_to_check = -1
        self.assertEqual(questions.prime_number(num_to_check), False)

    def test_primeNumber_5(self):
        num_to_check = 2
        self.assertEqual(questions.prime_number(num_to_check), True)

    def test_primeNumber_6(self):
        num_to_check = 100101
        self.assertEqual(questions.prime_number(num_to_check), False)


class TestPalindromeNum(unittest.TestCase):
    """
    1 Katas
    """

    def test_palindrome_1(self):
        num_to_check = 1441
        self.assertEqual(questions.palindrome_num(num_to_check), True)

    def test_palindrome_2(self):
        num_to_check = 123
        self.assertEqual(questions.palindrome_num(num_to_check), False)

    def test_palindrome_3(self):
        num_to_check = 12321123456
        self.assertEqual(questions.palindrome_num(num_to_check), False)

    def test_palindrome_4(self):
        num_to_check = 0
        self.assertEqual(questions.palindrome_num(num_to_check), True)

    def test_palindrome_5(self):
        num_to_check = -1
        self.assertEqual(questions.palindrome_num(num_to_check), False)

    def test_palindrome_6(self):
        num_to_check = 9
        self.assertEqual(questions.palindrome_num(num_to_check), True)

    def test_palindrome_7(self):
        num_to_check = 10
        self.assertEqual(questions.palindrome_num(num_to_check), False)


class TestPairMatch(unittest.TestCase):
    """
    3 Katas
    """

    def test_default(self):
        men = {"John": 20, "Abraham": 45}
        women = {"July": 18, "Kim": 26}
        result = ("John", "July")
        self.assertEqual(questions.pair_match(men, women), result)

    def test_empty(self):
        self.assertEqual(questions.pair_match({}, {}), ())

    def test_half_empty(self):
        men = {"John": 20, "Abraham": 45}
        self.assertEqual(questions.pair_match(men, {}), ())

    def test_half_empty2(self):
        women = {"July": 18, "Kim": 26}
        self.assertEqual(questions.pair_match({}, women), ())

    def test_identical_age(self):
        men = {"John": 20, "Abraham": 45}
        women = {"July": 18, "Kim": 20}
        result = ("John", "Kim")
        self.assertEqual(questions.pair_match(men, women), result)

    def test_large(self):
        men = {
            'John': 0, 'Michael': 3, 'David': 10,
            'James': 21, 'Robert': 36, 'William': 55,
            'Joseph': 78, 'Daniel': 105
        }
        women = {
            'Mary': 1, 'Jennifer': 6, 'Linda': 15,
            'Patricia': 28, 'Elizabeth': 45, 'Susan': 66,
            'Jessica': 91, 'Sarah': 120
        }
        result = ("John", "Mary")
        self.assertEqual(questions.pair_match(men, women), result)


class TestBadAverage(unittest.TestCase):
    """
    1 Katas
    """

    def test_empty(self):
        self.assertEqual(questions.bad_average(0, 0, 0), 0)

    def test_integer(self):
        self.assertEqual(questions.bad_average(1, 2, 3), 2)

    def test_large(self):
        self.assertEqual(questions.bad_average(10000, 20000, 30000), 20000)

    def test_fract(self):
        self.assertEqual(questions.bad_average(0.5, 1, 1.5), 1)

    def test_mixed(self):
        self.assertEqual(questions.bad_average(3, 5, 1.99), 3.33)

    def test_negative(self):
        self.assertEqual(questions.bad_average(-10, -20, -30), -20)


class TestBestStudent(unittest.TestCase):
    """
    1 Katas
    """

    def test_empty(self):
        self.assertEqual(questions.best_student({}), "")

    def test_default(self):
        students = {
            "Ben": 78,
            "Hen": 88,
            "Natan": 99,
            "Efraim": 65,
            "Rachel": 95
        }
        self.assertEqual(questions.best_student(students), "Natan")

    def test_negative(self):
        students = {
            "Ben": -78,
            "Hen": -88,
            "Natan": -99,
            "Efraim": -65,
            "Rachel": -95
        }
        self.assertEqual(questions.best_student(students), "Efraim")

    def test_fract(self):
        students = {
            "Ben": 3.5,
            "Hen": 88.95,
            "Natan": 88.2,
            "Efraim": -65.3,
            "Rachel": -95
        }
        self.assertEqual(questions.best_student(students), "Hen")


class TestPrintDictAsTable(unittest.TestCase):
    """
    1 Katas
    """

    def test_empty(self):
        result = "Key     Value\n-------------"
        self.assertEqual(questions.print_dict_as_table({}), result)

    def test_default(self):
        test_dict = {
            "Ben": 78,
            "Hen": 88,
            "Natan": 99,
            "Efraim": 65,
            "Rachel": 95
        }
        possibilities = [
            "Key     Value\n" +
            "-------------\n" +
            "Ben     78\n" +
            "Hen     88\n" +
            "Natan   99\n" +
            "Efraim  65\n" +
            "Rachel  95",
            "Key     Value\n" +
            "-------------\n" +
            "Ben\t78\n" +
            "Hen\t88\n" +
            "Natan\t99\n" +
            "Efraim\t65\n" +
            "Rachel\t95",
            "Key     Value\n" +
            "-------------\n" +
            "Ben\t\t78\n" +
            "Hen\t\t88\n" +
            "Natan\t99\n" +
            "Efraim\t65\n" +
            "Rachel\t95",
        ]
        self.assertTrue(questions.print_dict_as_table(test_dict) in possibilities)

    def test_negative(self):
        test_dict = {
            "Ben": -78,
            "Hen": -88,
            "Natan": -99,
            "Efraim": -65,
            "Rachel": -95
        }
        possibilities = [
            "Key     Value\n" +
            "-------------\n" +
            "Ben     -78\n" +
            "Hen     -88\n" +
            "Natan   -99\n" +
            "Efraim  -65\n" +
            "Rachel  -95",
            "Key     Value\n" +
            "-------------\n" +
            "Ben\t-78\n" +
            "Hen\t-88\n" +
            "Natan\t-99\n" +
            "Efraim\t-65\n" +
            "Rachel\t-95",
            "Key     Value\n" +
            "-------------\n" +
            "Ben\t\t-78\n" +
            "Hen\t\t-88\n" +
            "Natan\t-99\n" +
            "Efraim\t-65\n" +
            "Rachel\t-95",
        ]
        self.assertTrue(questions.print_dict_as_table(test_dict) in possibilities)


class TestMergeDicts(unittest.TestCase):
    """
    1 Katas
    """
    def test_empty(self):
        self.assertDictEqual(questions.merge_dicts({}, {}), {})

    def test_default(self):
        self.assertDictEqual(questions.merge_dicts({'a': 1}, {'b': 2}), {'a': 1, 'b': 2})

    def test_conflicts(self):
        dict1 = {
            'a': 1, 'b': 1, 'c': 1
        }
        dict2 = {
            'b': 2, 'c': 2, 'd': 2
        }
        result = {
            'a': 1, 'b': 2, 'c': 2, 'd': 2
        }
        self.assertDictEqual(questions.merge_dicts(dict1, dict2), result)

    def test_half_empty(self):
        dict1 = {
            'a': 1, 'b': 1, 'c': 1
        }
        self.assertDictEqual(questions.merge_dicts(dict1, {}), dict1)

    def test_half_empty2(self):
        dict2 = {
            'b': 2, 'c': 2, 'd': 2
        }
        self.assertDictEqual(questions.merge_dicts({}, dict2), dict2)


class TestSevenBoom(unittest.TestCase):
    """
    1 Katas
    """
    def test_zero(self):
        self.assertEqual(questions.seven_boom(0), [0])

    def test_one(self):
        self.assertEqual(questions.seven_boom(1), [])

    def test_default(self):
        result = [7, 14, 17, 21, 27, 28]
        self.assertEqual(questions.seven_boom(30), result)

    def test_no_boom(self):
        self.assertEqual(questions.seven_boom(6), [])

    def test_negative(self):
        result = [0, -7, -14, -17, -21, -27, -28]
        self.assertEqual(questions.seven_boom(-30), result)


class TestCaesarCipher(unittest.TestCase):
    """
    1 Katas
    """

    def test_empty(self):
        self.assertEqual(questions.caesar_cipher(''), '')

    def test_default(self):
        source = 'Fly Me To The Moon'
        result = 'Iob Ph Wr Wkh Prrq'
        self.assertEqual(questions.caesar_cipher(source), result)

    def test_all_lower(self):
        source = 'abcdefghijklmnopqrstuvwxyz'
        result = 'defghijklmnopqrstuvwxyzabc'
        self.assertEqual(questions.caesar_cipher(source), result)

    def test_all_upper(self):
        source = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = 'DEFGHIJKLMNOPQRSTUVWXYZABC'
        self.assertEqual(questions.caesar_cipher(source), result)


class TestSumOfDigits(unittest.TestCase):
    """
    1 Katas
    """

    def test_empty(self):
        self.assertEqual(questions.sum_of_digits(''), 0)

    def test_default(self):
        self.assertEqual(questions.sum_of_digits('2524'), 13)

    def test_default2(self):
        self.assertEqual(questions.sum_of_digits('00232'), 7)

    def test_zeros(self):
        self.assertEqual(questions.sum_of_digits('000000'), 0)

    def test_all_digits(self):
        self.assertEqual(questions.sum_of_digits('0123456789'), 45)


if __name__ == '__main__':
    import inspect
    import sys

    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))
