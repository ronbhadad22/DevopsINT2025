import os
import unittest
import shutil
import tarfile
import io
import contextlib  # Import module, not individual functions
import datetime as dt  # Import as dt to avoid docstring conflict
import json
import tempfile
import sys

# Direct import of local questions module
import questions

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import unittest_runner

# Import specific functions directly from questions module
from questions import replace_in_file
from questions import json_configs_merge
from questions import files_backup
from questions import most_frequent_name

testers = ['roee', 'david', 'tal gold']

class TestValidParentheses(unittest.TestCase):
    """
    2 Kata
    """


    def test_valid_strings(self):
        self.assertTrue(questions.valid_parentheses("[[{()}](){}]"))
        self.assertTrue(questions.valid_parentheses("()"))
        self.assertTrue(questions.valid_parentheses("{[()]}"))
        self.assertTrue(questions.valid_parentheses("([{}])"))
        self.assertTrue(questions.valid_parentheses(""))

    def test_invalid_strings(self):
        self.assertFalse(questions.valid_parentheses("]"))
        self.assertFalse(questions.valid_parentheses("[)"))
        self.assertFalse(questions.valid_parentheses("({)}"))
        self.assertFalse(questions.valid_parentheses("[({})]}"))
        self.assertFalse(questions.valid_parentheses("{[(])}"))

    def test_edge_cases(self):
        self.assertTrue(questions.valid_parentheses("()" * 50))
        self.assertFalse(questions.valid_parentheses(
            "[" * 50 + "]" * 50 + ")" * 50 + "(" * 50))

    def test_nested_invalid_string(self):
        self.assertFalse(questions.valid_parentheses("[{[())]}]"))

    def test_non_bracket_characters(self):
        self.assertFalse(questions.valid_parentheses("abc"))
        self.assertFalse(questions.valid_parentheses("(a)"))
        self.assertFalse(questions.valid_parentheses("(){}[]a"))


class TestFibonacciFixme(unittest.TestCase):
    """
    2 Kata
    """


    def test_fibonacci_fixme_first_two_terms(self):
        self.assertEqual(questions.fibonacci_fixme(1), 1)
        self.assertEqual(questions.fibonacci_fixme(2), 1)

    def test_fibonacci_fixme_valid_input(self):
        self.assertEqual(questions.fibonacci_fixme(3), 2)
        self.assertEqual(questions.fibonacci_fixme(4), 3)
        self.assertEqual(questions.fibonacci_fixme(5), 5)
        self.assertEqual(questions.fibonacci_fixme(6), 8)
        self.assertEqual(questions.fibonacci_fixme(7), 13)
        self.assertEqual(questions.fibonacci_fixme(8), 21)
        self.assertEqual(questions.fibonacci_fixme(9), 34)
        self.assertEqual(questions.fibonacci_fixme(10), 55)

    def test_fibonacci_fixme_large_input(self):
        self.assertEqual(questions.fibonacci_fixme(20), 6765)

    def test_fibonacci_fixme_invalid_input(self):
        with self.assertRaises(ValueError):
            questions.fibonacci_fixme(0)
        with self.assertRaises(ValueError):
            questions.fibonacci_fixme(-3)

    def test_fibonacci_fixme_non_integer_input(self):
        with self.assertRaises(TypeError):
            questions.fibonacci_fixme("5")
        with self.assertRaises(TypeError):
            questions.fibonacci_fixme(5.5)


class TestMostFrequentName(unittest.TestCase):
    """
    2 Kata
    """

    def create_temp_file(self, content):
        temp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        temp.write('\n'.join(content))
        temp.close()
        return temp.name

    def test_most_frequent_name(self):
        names = ["Alice", "Bob", "Alice", "Tawsha",
                 "Alice", "Bob", "Tawsha", "Tawsha"]
        file_path = self.create_temp_file(names)
        self.assertEqual(most_frequent_name(file_path), "Alice" or "Tawsha")
        os.remove(file_path)

    def test_single_name(self):
        file_path = self.create_temp_file(["OnlyName"])
        self.assertEqual(most_frequent_name(file_path), "OnlyName")
        os.remove(file_path)

    def test_all_unique_names(self):
        file_path = self.create_temp_file(["Ann", "Ben", "Carl"])
        result = most_frequent_name(file_path)
        self.assertIn(result, ["Ann", "Ben", "Carl"])
        os.remove(file_path)

    def test_empty_file(self):
        file_path = self.create_temp_file([])
        with self.assertRaises(ValueError):
            most_frequent_name(file_path)
        os.remove(file_path)


class TestFilesBackup(unittest.TestCase):
    """
    2 Kata
    """

    def setUp(self):
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)
        for i in range(3):
            with open(os.path.join(self.test_dir, f'test_file_{i}.txt'), 'w') as f:
                f.write(f'This is test file {i}')

    def tearDown(self):
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)

        today = dt.date.today().isoformat()
        backup_filename = f'backup_{os.path.basename(self.test_dir)}_{today}.tar.gz'
        if os.path.exists(backup_filename):
            os.remove(backup_filename)

    def test_backup_file_created(self):
        backup_file = files_backup(self.test_dir)

        today = dt.date.today().isoformat()
        expected_filename = f'backup_{os.path.basename(self.test_dir)}_{today}.tar.gz'
        self.assertEqual(backup_file, expected_filename)

        self.assertTrue(os.path.exists(backup_file))

        with tarfile.open(backup_file, "r:gz") as tar:
            names = tar.getnames()
            self.assertIn(f'test_file_0.txt', names[0])
            self.assertEqual(len(names), 3)


class TestReplaceInFile(unittest.TestCase):
    """
    2 Kata
    """

    def setUp(self):
        self.test_file = 'test_replace.txt'

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_replace_existing_text(self):
        with open(self.test_file, 'w') as f:
            f.write("This is a test file.\nContains text to be replaced.")

        replace_in_file(self.test_file, "text to be replaced", "new text")

        with open(self.test_file, 'r') as f:
            content = f.read()
        self.assertIn("new text", content)
        self.assertNotIn("text to be replaced", content)

    def test_replace_text_not_present(self):
        """Test trying to replace text that is not present in the file."""
        with open(self.test_file, 'w') as f:
            f.write("This is a test file.\nNothing here.")

        with open(self.test_file, 'r') as f:
            original_content = f.read()

        replace_in_file(self.test_file, "non-existent", "new text")

        with open(self.test_file, 'r') as f:
            updated_content = f.read()

        self.assertEqual(original_content, updated_content)

    def test_multiple_occurrences(self):
        with open(self.test_file, 'w') as f:
            f.write("repeat, repeat, repeat.")

        replace_in_file(self.test_file, "repeat", "done")

        with open(self.test_file, 'r') as f:
            content = f.read()

        self.assertEqual(content, "done, done, done.")


class TestJsonConfigsMerge(unittest.TestCase):
    """
    2 Kata
    """

    def setUp(self):
        self.temp_files = []
        self.temp_file_paths = []

        self.json_data_list = [
            {"a": 1, "b": 2},
            {"b": 20, "c": 30},
            {"d": 4}
        ]

        for data in self.json_data_list:
            temp = tempfile.NamedTemporaryFile(
                delete=False, suffix=".json", mode="w+")
            json.dump(data, temp)
            temp.close()
            self.temp_files.append(temp)
            self.temp_file_paths.append(temp.name)

    def tearDown(self):
        for file in self.temp_file_paths:
            if os.path.exists(file):
                os.remove(file)

    def test_merge_order_and_override(self):
        merged = json_configs_merge(*self.temp_file_paths)
        expected = {"a": 1, "b": 20, "c": 30, "d": 4}
        self.assertEqual(merged, expected)

    def test_merge_single_file(self):
        merged = json_configs_merge(self.temp_file_paths[0])
        self.assertEqual(merged, self.json_data_list[0])

    def test_merge_no_files(self):
        merged = json_configs_merge()
        self.assertEqual(merged, {})


class TestMonotonicArray(unittest.TestCase):
    """
    2 Kata
    """

    def test_strictly_increasing(self):
        self.assertTrue(questions.monotonic_array([1, 2, 3, 4]))

    def test_non_strictly_increasing(self):
        self.assertTrue(questions.monotonic_array([1, 2, 2, 3]))

    def test_strictly_decreasing(self):
        self.assertTrue(questions.monotonic_array([4, 3, 2, 1]))

    def test_non_strictly_decreasing(self):
        self.assertTrue(questions.monotonic_array([5, 5, 3, 1]))

    def test_all_equal(self):
        self.assertTrue(questions.monotonic_array([7, 7, 7, 7]))

    def test_not_monotonic_up_then_down(self):
        self.assertFalse(questions.monotonic_array([1, 3, 2]))

    def test_not_monotonic_down_then_up(self):
        self.assertFalse(questions.monotonic_array([3, 1, 2]))

    def test_not_monotonic_zigzag(self):
        self.assertFalse(questions.monotonic_array([1, 3, 2, 4]))

    def test_empty_list(self):
        self.assertTrue(questions.monotonic_array([]))

    def test_single_element(self):
        self.assertTrue(questions.monotonic_array([42]))

    def test_two_elements_increasing(self):
        self.assertTrue(questions.monotonic_array([1, 2]))

    def test_two_elements_decreasing(self):
        self.assertTrue(questions.monotonic_array([2, 1]))

    def test_two_elements_equal(self):
        self.assertTrue(questions.monotonic_array([5, 5]))

    def test_floats_increasing(self):
        self.assertTrue(questions.monotonic_array([1.1, 2.2, 3.3]))

    def test_floats_decreasing(self):
        self.assertTrue(questions.monotonic_array([3.3, 2.2, 1.1]))

    def test_floats_not_monotonic(self):
        self.assertFalse(questions.monotonic_array([1.1, 3.3, 2.2]))

    def test_monotonic_array_non_monotonic_list_mixed_sign(self):
        self.assertFalse(questions.monotonic_array([-5, -4, -3, 2, 1]))


class TestMatrixAvg(unittest.TestCase):
    """
    2 Kata
    """

    def test_matrix_average(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(questions.matrix_avg(matrix), 5)
        self.assertEqual(questions.matrix_avg(matrix,rows=[0,1]),3.5)
        self.assertEqual(questions.matrix_avg(matrix,rows=[2]), 8)
    
    def test_invalid_row_index(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        with self.assertRaises(IndexError):
            questions.matrix_avg(matrix, rows=[3])

class TestMergeSortedLists(unittest.TestCase):
    """
    2 Kata
    """

    def test_both_empty(self):
        self.assertEqual(questions.merge_sorted_lists([], []), [])

    def test_one_empty(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], []), [1, 2, 3])
        self.assertEqual(questions.merge_sorted_lists([], [4, 5, 6]), [4, 5, 6])

    def test_interleaved(self):
        self.assertEqual(questions.merge_sorted_lists([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])

    def test_all_first_smaller(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6])

    def test_all_first_larger(self):
        self.assertEqual(questions.merge_sorted_lists([7, 8, 9], [1, 2, 3]), [1, 2, 3, 7, 8, 9])

    def test_duplicates(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 2], [2, 3]), [1, 2, 2, 2, 3])

    def test_negatives(self):
        self.assertEqual(questions.merge_sorted_lists([-5, -3, 0], [-4, -2, 1]), [-5, -4, -3, -2, 0, 1])

    def test_all_same(self):
        self.assertEqual(questions.merge_sorted_lists([1, 1, 1], [1, 1]), [1, 1, 1, 1, 1])


class TestLongestCommonSubstring(unittest.TestCase):
    """
    2 Kata
    """
    def test_empty_strings(self):
        str1 = ''
        str2 = ''
        output = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), output)
    
    def test_one_empty_string(self):
        str1 = 'sdgdg'
        str2 = ''
        output = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), output)
        str1 = ''
        str2 = 'fsdhh'
        output = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), output)
    
    def test_no_common_substring(self):
        str1 = 'qwer'
        str2 = 'zxvn'
        output = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), output)
    
    def test_common_substring(self):
        str1 = 'Introduced in 1991, The Linux kernel is an amazing software'
        str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'
        output = 'The Linux kernel is a'
        self.assertEqual(questions.longest_common_substring(str1, str2), output)

class TestLongestCommonPrefix(unittest.TestCase):
    """
    2 Kata
    """
    
    def test_empty_strings(self):
        str1 = ''
        str2 = ''
        output = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), output)

    def test_one_empty_string(self):
        str1 = 'sfsffa'
        str2 = ''
        output = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), output)
        str1 = ''
        str2 = 'sfsffa'
        output = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), output)
    
    def test_no_common_prefix(self):
        str1 = 'acccc'
        str2 = 'bcccc'
        output = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), output)
    
    def test_common_prefix(self):
        str1 = 'The Linux kernel is an amazing software'
        str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'
        output = 'The Linux kernel is a'
        self.assertEqual(questions.longest_common_prefix(str1, str2), output)
    
    
    

class TestRotateMatrix(unittest.TestCase):
    """
    2 Kata
    """

    def test_empty_matrix(self):
        input = []
        outpoot = []
        self.assertEqual(questions.rotate_matrix(input), outpoot)
    
    def test_one_column_matrix(self):
        input = [[1], [2], [3], [4]]
        outpoot = [[4, 3, 2, 1]]
        self.assertEqual(questions.rotate_matrix(input), outpoot)
    
    def test_one_row_matrix(self):
        input = [[1, 2, 3, 4]]
        outpoot = [[1], [2], [3], [4]]
        self.assertEqual(questions.rotate_matrix(input), outpoot)
    
    def test_random_matrix(self):
        input = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        outpoot = [[10, 7, 4, 1], [11, 8, 5, 2], [12, 9, 6, 3]]
        self.assertEqual(questions.rotate_matrix(input), outpoot)

class TestIsValidEmail(unittest.TestCase):
    """
    2 Kata
    """

    def test_valid_emails(self):
        self.assertTrue(questions.is_valid_email('roieharkavi@gmail.com'))
        self.assertTrue(questions.is_valid_email('tal.gold@gmail.com'))
        self.assertTrue(questions.is_valid_email('david_levi@gmail.com'))
        self.assertTrue(questions.is_valid_email('roieharkavi1@gmail.com'))
        self.assertTrue(questions.is_valid_email('1talgold@gmail.com'))
        self.assertTrue(questions.is_valid_email('roieharkavi@walla.co.il'))
    
    def test_invalid_emails(self):
        self.assertFalse(questions.is_valid_email(''))
        self.assertFalse(questions.is_valid_email('roieharkavigmail.com'))
        self.assertFalse(questions.is_valid_email('@gmail.com'))
        self.assertFalse(questions.is_valid_email('talgold!@gmail.com'))
        self.assertFalse(questions.is_valid_email('davidlevi@@gmail.com'))
        self.assertFalse(questions.is_valid_email('roieharkavi@dgdhh'))

class TestPascalTriangle(unittest.TestCase):
    """
    2 Kata
    """
    
    def test_empty_triangle(self):
        input = 0
        outpoot = ''
        self.assertEqual(questions.pascal_triangle(input), outpoot)
    
    def test_3_rows_triangle(self):
        input = 3
        outpoot = '1\n1 1\n1 2 1'
        self.assertEqual(questions.pascal_triangle(input), outpoot)

    def test_10_rows_triangle(self):
        input = 10
        outpoot = '1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n1 6 15 20 15 6 1\n1 7 21 35 35 21 7 1\n1 8 28 56 70 56 28 8 1\n1 9 36 84 126 126 84 36 9 1'
        self.assertEqual(questions.pascal_triangle(input), outpoot)


class TestListFlatten(unittest.TestCase):
    """
    2 Kata
    """
    
    def test_empty_list(self):
        input = []
        output = []
        self.assertEqual(questions.list_flatten(input), output)
    
    def test_empty_nested_lists(self):
        input = [[[[], [[]]]]]
        output = []
        self.assertEqual(questions.list_flatten(input), output)

    def test_regular_list(self):
        input = [1,2,3,4,5]
        output = [1,2,3,4,5]
        self.assertEqual(questions.list_flatten(input), output)

    def test_nested_lists(self):
        input = [1,[[],[2],[3,4]],5]
        output = [1,2,3,4,5]
        self.assertEqual(questions.list_flatten(input), output)

class TestStrCompression(unittest.TestCase):
    """
    2 Kata
    """

    def test_empty_string(self):
        input = ''
        output = []
        self.assertEqual(questions.str_compression(input), output)

    def test_one_letter_each_string(self):
        input = 'abcd'
        output = ['a','b','c','d']
        self.assertEqual(questions.str_compression(input), output)
    
    def test_one_letter_each_with_1_digit_string(self):
        input = 'abcd'
        output = ['a',1,'b',1,'c',1,'d',1]
        self.assertEqual(questions.str_compression(input), output)
    
    def test_multipule_letters_string(self):
        input = 'aaabbcccdeeeef'
        output = ['a',3,'b',2,'c',3,'d',1,'e',4,'f']
        self.assertEqual(questions.str_compression(input), output)

class TestStrongPass(unittest.TestCase):
    """
    2 Kata
    """
    
    def test_valid_passwords(self):
        self.assertTrue(questions.strong_pass('Ab123!'))
        self.assertTrue(questions.strong_pass('@sxF8ssH'))
        self.assertTrue(questions.strong_pass('11111Aq#'))
    
    def test_invalid_passwords(self):
        self.assertFalse(questions.strong_pass(''))
        self.assertFalse(questions.strong_pass('Aa12!'))
        self.assertFalse(questions.strong_pass('abc12@'))
        self.assertFalse(questions.strong_pass('ABC12#'))
        self.assertFalse(questions.strong_pass('Abc!@#'))
        self.assertFalse(questions.strong_pass('Abc123'))
        self.assertFalse(questions.strong_pass('Abc12='))


if __name__ == '__main__':
    import inspect
    import sys
    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))