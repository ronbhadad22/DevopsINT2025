import unittest
from python_katas.kata_1.questions import *


class TestSumOfElement(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum_of_element([1, 2]), 3)
        self.assertEqual(sum_of_element([]), 0)

class TestVerbing(unittest.TestCase):
    def test_short_word(self):
        self.assertEqual(verbing("go"), "go")

    def test_add_ing(self):
        self.assertEqual(verbing("walk"), "walking")

    def test_add_ly(self):
        self.assertEqual(verbing("swimming"), "swimmingly")

class TestWordsConcatenation(unittest.TestCase):
    def test_words(self):
        self.assertEqual(words_concatenation(['take', 'me', 'home']), 'take me home')
        self.assertEqual(words_concatenation([]), '')

class TestReverseWordsConcatenation(unittest.TestCase):
    def test_reverse(self):
        self.assertEqual(reverse_words_concatenation(['take', 'me', 'home']), 'home me take')

class TestIsUniqueString(unittest.TestCase):
    def test_unique(self):
        self.assertTrue(is_unique_string("abcde"))
        self.assertFalse(is_unique_string("aabc"))
        self.assertTrue(is_unique_string(""))

class TestListDiff(unittest.TestCase):
    def test_diff(self):
        self.assertEqual(list_diff([1, 2, 3]), [None, 1, 1])
        self.assertEqual(list_diff([]), [])
        self.assertEqual(list_diff([5]), [None])

class TestPrimeNumber(unittest.TestCase):
    def test_prime(self):
        self.assertTrue(prime_number(7))
        self.assertFalse(prime_number(4))
        self.assertFalse(prime_number(1))

class TestPalindromeNum(unittest.TestCase):
    def test_palindrome(self):
        self.assertTrue(palindrome_num(1221))
        self.assertFalse(palindrome_num(123))

class TestPairMatch(unittest.TestCase):
    def test_match(self):
        men = {"John": 20, "Abraham": 45}
        women = {"July": 18, "Kim": 26}
        self.assertEqual(pair_match(men, women), ("John", "July"))

class TestBadAverage(unittest.TestCase):
    def test_average(self):
        self.assertAlmostEqual(bad_average(1, 2, 3), 2.0)

class TestBestStudent(unittest.TestCase):
    def test_best(self):
        data = {
            "Ben": 78,
            "Hen": 88,
            "Natan": 99,
            "Efraim": 65,
            "Rachel": 95
        }
        self.assertEqual(best_student(data), "Natan")

class TestMergeDicts(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(merge_dicts({'a': 1}, {'b': 2}), {'a': 1, 'b': 2})

class TestSevenBoom(unittest.TestCase):
    def test_boom(self):
        self.assertEqual(seven_boom(30), [7, 14, 17, 21, 27, 28])

class TestCaesarCipher(unittest.TestCase):
    def test_cipher(self):
        self.assertEqual(caesar_cipher("Fly Me To The Moon"), "Iob Ph Wr Wkh Prrq")

class TestSumOfDigits(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum_of_digits("2524"), 13)
        self.assertEqual(sum_of_digits("00232"), 7)
        self.assertEqual(sum_of_digits(""), 0)

if __name__ == '__main__':
    unittest.main()