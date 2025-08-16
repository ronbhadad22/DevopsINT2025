import unittest
import io
from contextlib import redirect_stdout
import kata_questions_1 as questions


class TestAllFunctions(unittest.TestCase):

    # q1
    def test_sum_of_element(self):
        self.assertEqual(questions.sum_of_element([]), 0)
        self.assertEqual(questions.sum_of_element([1]), 1)
        self.assertEqual(questions.sum_of_element([1, 2, 3]), 6)
        self.assertEqual(questions.sum_of_element([-2, 5, -3]), 0)

    # q2
    def test_verbing(self):
        self.assertEqual(questions.verbing('teach'), 'teaching')
        self.assertEqual(questions.verbing('swimming'), 'swimmingly')
        self.assertEqual(questions.verbing('do'), 'do')
        self.assertEqual(questions.verbing('ing'), 'ingly')

    # q3 (missing in your earlier tests)
    def test_words_concatenation(self):
        self.assertEqual(questions.words_concatenation(['take', 'me', 'home']), 'take me home')
        self.assertEqual(questions.words_concatenation([]), '')
        self.assertEqual(questions.words_concatenation(['solo']), 'solo')

    # q4
    def test_reverse_words_concatenation(self):
        self.assertEqual(questions.reverse_words_concatenation(['take', 'me', 'home']), 'home me take')
        self.assertEqual(questions.reverse_words_concatenation([]), '')
        self.assertEqual(questions.reverse_words_concatenation(['solo']), 'solo')

    # q5 (name aligned with original)
    def test_is_unique_string(self):
        self.assertTrue(questions.is_unique_string('abcd'))
        self.assertFalse(questions.is_unique_string('aaabcd'))
        self.assertTrue(questions.is_unique_string(''))

    # q6 (name aligned with original)
    def test_list_diff(self):
        self.assertEqual(questions.list_diff([]), [])
        self.assertEqual(questions.list_diff([1]), [None])
        self.assertEqual(questions.list_diff([1, 2, 3]), [None, 1, 1])
        self.assertEqual(questions.list_diff([1, 5, 0, 4, 1, 1, 1]), [None, 4, -5, 4, -3, 0, 0])

    # q7 (name aligned with original)
    def test_prime_number(self):
        self.assertTrue(questions.prime_number(2))
        self.assertTrue(questions.prime_number(5))
        self.assertFalse(questions.prime_number(4))
        self.assertFalse(questions.prime_number(1))
        self.assertFalse(questions.prime_number(0))
        self.assertFalse(questions.prime_number(-7))
        self.assertTrue(questions.prime_number(97))

    # q8 (name aligned with original)
    def test_palindrome_num(self):
        self.assertTrue(questions.palindrome_num(1441))
        self.assertFalse(questions.palindrome_num(123))
        self.assertTrue(questions.palindrome_num(7))

    # q9 (name aligned with original)
    def test_pair_match(self):
        self.assertEqual(questions.pair_match({"Tom": 20}, {"Anna": 21}), ("Tom", "Anna"))
        self.assertEqual(questions.pair_match({}, {"Anna": 30}), None)
        self.assertEqual(questions.pair_match({"Tom": 20}, {}), None)
        # tie case (either valid pair accepted if same diff) – check diff, not exact names
        men = {"A": 20, "B": 30}
        women = {"C": 25}
        pair = questions.pair_match(men, women)
        self.assertIn(pair, {("A", "C"), ("B", "C")})
        self.assertEqual(abs(men[pair[0]] - women[pair[1]]), 5)

    # q10 (bad_average should be fixed to true average)
    def test_bad_average_fixed(self):
        self.assertAlmostEqual(questions.bad_average(1, 2, 3), 2.0)
        self.assertAlmostEqual(questions.bad_average(3, 9, 0), 4.0)
        self.assertAlmostEqual(questions.bad_average(-3, 3, 6), 2.0)

    # q11 (name aligned with original)
    def test_best_student(self):
        grades = {"Ben": 78, "Hen": 88, "Natan": 99, "Efraim": 65, "Rachel": 95}
        self.assertEqual(questions.best_student(grades), "Natan")
        self.assertIsNone(questions.best_student({}))

    # q12
    def test_print_dict_as_table(self):
        data = {"Ben": 78, "Hen": 88}
        expected = "Key\tValue\n-------------\nBen\t78\nHen\t88"
        with io.StringIO() as buf, redirect_stdout(buf):
            questions.print_dict_as_table(data)
            output = buf.getvalue().strip()
        self.assertEqual(output, expected)

    # q13
    def test_merge_dicts(self):
        dict1 = {'a': 1}
        dict2 = {'b': 2}
        merged = questions.merge_dicts(dict1, dict2)
        self.assertEqual(merged, {'a': 1, 'b': 2})
        self.assertEqual(dict1, {'a': 1, 'b': 2})  # ensure mutated as spec

    # q14
    def test_seven_boom(self):
        self.assertEqual(questions.seven_boom(30), [7, 14, 17, 21, 27, 28])
        self.assertEqual(questions.seven_boom(0), [])
        self.assertEqual(questions.seven_boom(7), [7])
        self.assertEqual(questions.seven_boom(1), [])

    # q15
    def test_caesar_cipher(self):
        self.assertEqual(questions.caesar_cipher('Fly Me To The Moon'), 'Iob Ph Wr Wkh Prrq')
        self.assertEqual(questions.caesar_cipher('abc xyz'), 'def abc')
        self.assertEqual(questions.caesar_cipher('ZzAa'), 'CcDd')
        self.assertEqual(questions.caesar_cipher('Hello, World! 123'), 'Khoor, Zruog! 123')

    # q16
    def test_sum_of_digits(self):
        self.assertEqual(questions.sum_of_digits('2524'), 13)
        self.assertEqual(questions.sum_of_digits(''), 0)
        self.assertEqual(questions.sum_of_digits('00232'), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
