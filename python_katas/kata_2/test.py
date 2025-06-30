import os
import unittest
import shutil
import tarfile
import io
from contextlib import redirect_stdout
from datetime import datetime
from python_katas.kata_2 import questions
from python_katas.utils import unittest_runner

testers = ['ofri','denis','ron']

class TestValidParentheses(unittest.TestCase):
    """
    3 Katas
    """
    def test_valid_strings(self):
        self.assertTrue(questions.valid_parentheses("[[{()}](){}]"))
        self.assertTrue(questions.valid_parentheses("()"))
        self.assertTrue(questions.valid_parentheses(""))
        self.assertTrue(questions.valid_parentheses("{[()]}"))
        self.assertTrue(questions.valid_parentheses("([{}])"))

    def test_invalid_strings(self):
        self.assertFalse(questions.valid_parentheses("]"))
        self.assertFalse(questions.valid_parentheses("[)"))
        self.assertFalse(questions.valid_parentheses("({)}"))
        self.assertFalse(questions.valid_parentheses("[({})]}"))
        self.assertFalse(questions.valid_parentheses("{[(])}"))

    def test_edge_cases(self):
        self.assertTrue(questions.valid_parentheses("()" * 50))
        self.assertTrue(questions.valid_parentheses(""))
        self.assertFalse(questions.valid_parentheses(
            "[" * 50 + "]" * 50 + ")" * 50 + "(" * 50))

    def test_nested_invalid_string(self):
        self.assertFalse(questions.valid_parentheses("[{[())]}]"))

class TestFibonacciFixme(unittest.TestCase):
    """
    2 Katas
    """

    def test_fibonacci_fixme_first_two_terms(self):
        # Test case for the first two Fibonacci terms
        self.assertEqual(questions.fibonacci_fixme(1), 1)
        self.assertEqual(questions.fibonacci_fixme(2), 1)

    def test_fibonacci_fixme_valid_input(self):
        # Test case for valid input values
        self.assertEqual(questions.fibonacci_fixme(3), 2)
        self.assertEqual(questions.fibonacci_fixme(4), 3)
        self.assertEqual(questions.fibonacci_fixme(5), 5)
        self.assertEqual(questions.fibonacci_fixme(6), 8)
        self.assertEqual(questions.fibonacci_fixme(7), 13)
        self.assertEqual(questions.fibonacci_fixme(8), 21)
        self.assertEqual(questions.fibonacci_fixme(9), 34)
        self.assertEqual(questions.fibonacci_fixme(10), 55)

    def test_fibonacci_fixme_large_input(self):
        # Test case for large input value
        # We choose a relatively small large input value for efficiency
        self.assertEqual(questions.fibonacci_fixme(20), 6765)

class TestMostFrequentName(unittest.TestCase):
    """
    2 Katas
    """
    def test_most_frequent_name(self):
        file_path = "names.txt"  # Adjust the file path accordingly
        expected_result = "Tawsha"
        self.assertEqual(questions.most_frequent_name(file_path), expected_result)

    def test_file_existence(self):
        # Specify the file path
        file_path = 'names.txt'
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        # Assert that the file exists
        self.assertTrue(file_exists, f"File '{file_path}' does not exist in the directory.")

    def test_empty_file(self):
        # Specify the file path
        file_path = 'names.txt'

        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        self.assertTrue(file_exists, f"File '{file_path}' does not exist in the directory.")

        # Check if the file is empty
        file_empty = os.stat(file_path).st_size == 0
        self.assertFalse(file_empty, f"File '{file_path}' is empty.")

class TestFilesBackup(unittest.TestCase):
    """
    3 Katas
    """
    # Test cases for the files_backup function
    def setUp(self):
        # Define the test directory attribute
        self.test_dir = 'test_directory'
        # Check if the test directory already exists
        if not os.path.exists(self.test_dir):
            # Create a temporary directory for testing
            os.makedirs(self.test_dir)
            # Create some test files inside the directory
            for i in range(3):
                with open(os.path.join(self.test_dir, f'test_file_{i}.txt'), 'w') as f:
                    f.write(f'This is test file {i}')

    def tearDown(self):
        # Remove the temporary directory and its contents after testing
        shutil.rmtree(self.test_dir)

    def test_backup_file_name_format(self):
        # Test if the backup file name follows the correct format
        backup_file_name = questions.files_backup(self.test_dir)
        expected_format = f'backup_{os.path.basename(os.path.normpath(self.test_dir))}_\\d{{4}}-\\d{{2}}-\\d{{2}}.tar.gz'
        self.assertRegex(backup_file_name, expected_format)

    def test_backup_file_created(self):
        # Test if the backup file is created in the specified directory
        backup_file_name = questions.files_backup(self.test_dir)
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(self.test_dir), backup_file_name)))

    def test_correct_backup_file_name(self):
        # Test if the function returns the correct backup file name
        backup_file_name = questions.files_backup(self.test_dir)
        expected_name = f'backup_{os.path.basename(os.path.normpath(self.test_dir))}_{datetime.now().strftime("%Y-%m-%d")}.tar.gz'
        self.assertEqual(backup_file_name, expected_name)

    def test_backup_file_validity(self):
        # Test if the backup file is a valid .tar.gz archive
        backup_file_name = questions.files_backup(self.test_dir)
        with tarfile.open(backup_file_name, 'r:gz') as tar:
            self.assertIsNotNone(tar)

class TestReplaceInFile(unittest.TestCase):
    """
    2 Katas
    """

    def test_replace_existing_text(self):
        """Test replacing existing text in the file."""
        test_file_name = 'test_file.txt'
        with open(test_file_name, 'w') as f:
            f.write("This is a test file.\nContains text to be replaced.")

        questions.replace_in_file(test_file_name, "text to be replaced", "new text")

        with open(test_file_name, 'r') as f:
            content = f.read()
        self.assertIn("new text", content)

        os.remove(test_file_name)  # Cleanup

    def test_replace_text_not_present(self):
        """Test trying to replace text that is not present in the file."""
        test_file_name = 'test_file.txt'
        with open(test_file_name, 'w') as f:
            f.write("This is a test file.\nContains text to be replaced.")

        original_content = None
        with open(test_file_name, 'r') as f:
            original_content = f.read()

        questions.replace_in_file(test_file_name, "non-existent text", "new text")

        with open(test_file_name, 'r') as f:
            new_content = f.read()

        self.assertEqual(original_content, new_content)

        os.remove(test_file_name)  # Cleanup

    def test_multiple_occurrences(self):
        """Test replacing multiple occurrences of a text."""
        test_file_name = 'test_file.txt'
        with open(test_file_name, 'w') as f:
            f.write("Repeat, repeat, repeat.")

        questions.replace_in_file(test_file_name, "repeat", "done")

        with open(test_file_name, 'r') as f:
            content = f.read()

        self.assertEqual(content, "Repeat, done, done.")

        os.remove(test_file_name)  # Cleanup

class TestJsonConfigsMerge(unittest.TestCase):
    """
    2 Katas
    """
    def test_merge_json_files(self):
        # Test merging JSON files
        merged_json = questions.json_configs_merge('default.json', 'local.json')
        # Assert that the merged data is not empty
        self.assertTrue(merged_json)

class TestMonotonicArray(unittest.TestCase):
    """
    1 Katas
        """

    def test_monotonic_array_increasing(self):
        # Test case for a monotonically increasing list
        self.assertTrue(questions.monotonic_array([1, 2, 3, 4, 5]))

    def test_monotonic_array_decreasing(self):
        # Test case for a monotonically decreasing list
        self.assertTrue(questions.monotonic_array([5, 4, 3, 2, 1]))

    def test_monotonic_array_nonstrictly_increasing(self):
        # Test case for a non-strictly increasing list
        self.assertTrue(questions.monotonic_array([1, 2, 2, 3, 4]))

    def test_monotonic_array_nonstrictly_decreasing(self):
        # Test case for a non-strictly decreasing list
        self.assertTrue(questions.monotonic_array([5, 4, 3, 3, 2]))

    def test_monotonic_array_empty_list(self):
        # Test case for an empty list
        self.assertTrue(questions.monotonic_array([]))

    def test_monotonic_array_single_element_list(self):
        # Test case for a single-element list
        self.assertTrue(questions.monotonic_array([5]))

    def test_monotonic_array_with_repeated_elements(self):
        # Test case for a list with repeated elements
        self.assertTrue(questions.monotonic_array([1, 1, 1, 1, 1]))

    def test_monotonic_array_with_alternating_elements(self):
        # Test case for a list with alternating elements
        self.assertFalse(questions.monotonic_array([1, 3, 2, 4, 3]))

    def test_monotonic_array_with_constant_elements(self):
        # Test case for a list with constant elements
        self.assertTrue(questions.monotonic_array([2, 2, 2, 2, 2]))

    def test_monotonic_array_float_numbers(self):
        # Test case for a list with floating-point numbers
        self.assertTrue(questions.monotonic_array([1.1, 2.2, 3.3, 4.4]))

    def test_monotonic_array_mixed_float_and_int(self):
        # Test case for a list with mixed floating-point and integer numbers
        self.assertTrue(questions.monotonic_array([1, 2.5, 3, 4.7]))

    def test_monotonic_array_non_monotonic_list(self):
        # Test case for a non-monotonic list
        self.assertFalse(questions.monotonic_array([1, 3, 2, 5, 4]))

    def test_monotonic_array_non_monotonic_list_negative_numbers(self):
        # Test case for a non-monotonic list with negative numbers
        self.assertFalse(questions.monotonic_array([5, 4, -3, 2, 1]))

    def test_monotonic_array_non_monotonic_list_mixed_sign(self):
        # Test case for a non-monotonic list with mixed signs
        self.assertFalse(questions.monotonic_array([-5, -4, -3, 2, 1]))

class TestMatrixAvg(unittest.TestCase):
    """
    2 Katas
    """

    def test_full_matrix_average(self):
        """Tests the average calculation of all elements in the matrix."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(questions.matrix_avg(matrix), 5)

    def test_single_row_average(self):
        """Tests the average calculation of a single specified row."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        self.assertEqual(questions.matrix_avg(matrix, rows=[1]), 5)

    def test_multiple_rows_average(self):
        """Tests the average calculation when multiple rows are specified."""
        matrix = [
            [2, 4, 6],
            [1, 3, 5],
            [7, 9, 11]
        ]
        self.assertEqual(questions.matrix_avg(matrix, rows=[0, 2]), 6.5)

    def test_invalid_row_index(self):
        """Tests the average calculation with an invalid row index."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        # Expecting a failure or specific handling of invalid row index
        with self.assertRaises(IndexError):
            questions.matrix_avg(matrix, rows=[3])

class TestMergeSortedLists(unittest.TestCase):
    """
    1 Katas
    """

    def test_empty_lists(self):
        self.assertEqual(questions.merge_sorted_lists([], []), [])

    def test_one_empty_list(self):
        self.assertEqual(questions.merge_sorted_lists([], [1, 2, 3]), [1, 2, 3])
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], []), [1, 2, 3])

    def test_both_lists_have_elements(self):
        self.assertEqual(questions.merge_sorted_lists([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6])
        self.assertEqual(questions.merge_sorted_lists([2, 4, 6], [1, 3, 5]), [1, 2, 3, 4, 5, 6])

    def test_lists_with_duplicates(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 2, 3], [2, 3, 4, 4]), [1, 2, 2, 2, 3, 3, 4, 4])

    def test_lists_with_negative_numbers(self):
        self.assertEqual(questions.merge_sorted_lists([-3, -2, -1], [-4, -3, -2]), [-4, -3, -3, -2, -2, -1])

    def test_one_list_is_prefix_of_other(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], [1, 2, 3, 4, 5]), [1, 1, 2, 2, 3, 3, 4, 5])
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3, 4, 5], [1, 2, 3]), [1, 1, 2, 2, 3, 3, 4, 5])

    def test_already_merged_lists(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6])

    def test_one_element_list(self):
        self.assertEqual(questions.merge_sorted_lists([5], [1, 2, 3]), [1, 2, 3, 5])
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], [5]), [1, 2, 3, 5])

    def test_both_lists_have_same_elements(self):
        self.assertEqual(questions.merge_sorted_lists([1, 2, 3], [1, 2, 3]), [1, 1, 2, 2, 3, 3])

    def test_large_lists(self):
        self.assertEqual(questions.merge_sorted_lists(list(range(1000000)), list(range(1000000, 2000000))),
                         list(range(2000000)))

class TestLongestCommonSubstring(unittest.TestCase):
    """
    4 Katas
    """

    def test_basic_example(self):
        str1 = 'Introduced in 1991, The Linux kernel is an amazing software'
        str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'
        expected_result = 'The Linux kernel is a'
        self.assertEqual(questions.longest_common_substring(str1, str2), expected_result)

    def test_empty_strings(self):
        str1 = ''
        str2 = ''
        expected_result = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), expected_result)

    def test_no_common_substring(self):
        str1 = 'abcdef'
        str2 = 'ghijkl'
        expected_result = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), expected_result)

    def test_one_empty_string(self):
        str1 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'
        str2 = ''
        expected_result = ''
        self.assertEqual(questions.longest_common_substring(str1, str2), expected_result)

    def test_characters_common(self):
        str1 = 'abcdefg'
        str2 = 'xyzdefuvw'
        expected_result = 'def'
        self.assertEqual(questions.longest_common_substring(str1, str2), expected_result)

    def test_long_common_substring(self):
        str1 = 'abcdefg' * 100
        str2 = 'xyzdefuvw' * 100
        expected_result = 'def'
        self.assertEqual(questions.longest_common_substring(str1, str2), expected_result)

class TestLongestCommonPrefix(unittest.TestCase):
    """
    1 Katas
    """

    def test_common_prefix(self):
        str1 = 'The Linux kernel is an amazing software'
        str2 = 'The Linux kernel is a mostly free and open-source, monolithic, modular, multitasking, Unix-like operating system kernel.'
        expected_result = 'The Linux kernel is a'
        self.assertEqual(questions.longest_common_prefix(str1, str2), expected_result)

    def test_no_common_prefix(self):
        str1 = 'apple'
        str2 = 'banana'
        expected_result = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), expected_result)

    def test_one_empty_string(self):
        str1 = 'example'
        str2 = ''
        expected_result = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), expected_result)

    def test_both_empty_strings(self):
        str1 = ''
        str2 = ''
        expected_result = ''
        self.assertEqual(questions.longest_common_prefix(str1, str2), expected_result)

    def test_one_char_string(self):
        str1 = 'a'
        str2 = 'ab'
        expected_result = 'a'
        self.assertEqual(questions.longest_common_prefix(str1, str2), expected_result)

    def test_both_same_strings(self):
        str1 = 'hello'
        str2 = 'hello'
        expected_result = 'hello'
        self.assertEqual(questions.longest_common_prefix(str1, str2), expected_result)

class TestRotateMatrix(unittest.TestCase):
    """
    2 Katas
    """

    def test_3x3_matrix(self):
        mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected = [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
        self.assertEqual(questions.rotate_matrix(mat), expected, "3x3 matrix rotation failed")

    def test_4x3_matrix(self):
        mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        expected = [[10, 7, 4, 1], [11, 8, 5, 2], [12, 9, 6, 3]]
        self.assertEqual(questions.rotate_matrix(mat), expected, "4x3 matrix rotation failed")

    def test_single_row(self):
        mat = [[1, 2, 3, 4]]
        expected = [[1], [2], [3], [4]]
        self.assertEqual(questions.rotate_matrix(mat), expected, "Single row rotation failed")

    def test_single_column(self):
        mat = [[1], [2], [3], [4]]
        expected = [[4, 3, 2, 1]]
        self.assertEqual(questions.rotate_matrix(mat), expected, "Single column rotation failed")

    def test_empty_matrix(self):
        mat = []
        expected = []
        self.assertEqual(questions.rotate_matrix(mat), expected, "Empty matrix rotation failed")

class TestIsValidEmail(unittest.TestCase):
    """
    3 Katas
    """

    def test_valid_emails(self):
        # Test case for valid email addresses
        self.assertTrue(questions.is_valid_email('john.doe@gmail.com'))
        self.assertTrue(questions.is_valid_email('john_doe@gmail.com'))
        self.assertTrue(questions.is_valid_email('user13@gmail.com'))
        self.assertTrue(questions.is_valid_email('13user@gmail.com'))
        self.assertTrue(questions.is_valid_email('user@support.google.com'))
        self.assertTrue(questions.is_valid_email('user@example.co.uk'))

    def test_invalid_email_formats(self):
        # Test case for invalid email formats
        self.assertFalse(questions.is_valid_email('invalid_email'))  # Missing @ symbol
        self.assertFalse(questions.is_valid_email('user.gmail.com'))  # Missing @ symbol
        self.assertFalse(questions.is_valid_email('user@gmail'))  # Missing domain extension
        self.assertFalse(questions.is_valid_email('user@gmail@com'))  # Multiple @ symbols

    def test_invalid_characters_in_email(self):
        # Test case for email addresses with invalid characters
        self.assertFalse(questions.is_valid_email('user!@gmail.com'))  # Invalid character (!) in username
        self.assertFalse(questions.is_valid_email('user123@gmail!com'))  # Invalid character (!) in domain

    def test_invalid_domain_resolution(self):
        # Test case for email addresses with domain names that do not resolve to an actual IP address
        self.assertFalse(questions.is_valid_email('user@gmail.invalid'))  # Invalid domain extension

    def test_combinations_of_valid_and_invalid_characters(self):
        # Test case for email addresses with different combinations of valid and invalid characters
        self.assertFalse(questions.is_valid_email('!user@gmail.com'))  # Invalid character (!) in username
        self.assertFalse(questions.is_valid_email('user@gmail!.com'))  # Invalid character (!) in domain
        self.assertFalse(questions.is_valid_email('user@gmail.com!'))  # Invalid character (!) in domain

class TestPascalTriangle(unittest.TestCase):
    """
     3 Katas
     """

    def test_pascal_triangle_identity(self):
        # Define expected Pascal's triangles for the first 10 lines
        expected_triangles = [
            [[1]],
            [[1], [1, 1]],
            [[1], [1, 1], [1, 2, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1],
             [1, 7, 21, 35, 35, 21, 7, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1],
             [1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1]],
            [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1],
             [1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1], [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]]
        ]

        # Test for the first 10 lines to validate the identity property of Pascal's Triangle
        for n in range(10):
            # Redirect stdout to capture printed output
            with io.StringIO() as buf, redirect_stdout(buf):
                questions.pascal_triangle(n + 1)
                printed_output = buf.getvalue()

            # Parse printed output into a list of lists
            printed_triangle = [list(map(int, line.split())) for line in printed_output.strip().split('\n')]

            # Compare printed triangle with expected triangle
            self.assertEqual(printed_triangle, expected_triangles[n])

class TestListFlatten(unittest.TestCase):
    """
    2 Katas
    """

    def test_flat_list(self):
        input_list = [1, 2, 3, 4]
        expected_output = [1, 2, 3, 4]
        self.assertEqual(questions.list_flatten(input_list), expected_output)

    def test_nested_list(self):
        input_list = [1, [], [2, [3, 4], 5], 6]
        expected_output = [1, 2, 3, 4, 5, 6]
        self.assertEqual(questions.list_flatten(input_list), expected_output)

    def test_empty_list(self):
        input_list = []
        expected_output = []
        self.assertEqual(questions.list_flatten(input_list), expected_output)

    def test_mixed_types(self):
        input_list = [1, [2, 'a', [3.5, 4]], 5]
        expected_output = [1, 2, 'a', 3.5, 4, 5]
        self.assertEqual(questions.list_flatten(input_list), expected_output)

    def test_large_nested_list(self):
        input_list = [1, [2, [3, [4, [5, [6, [7, [8, [9, [10]]]]]]]]]]
        expected_output = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(questions.list_flatten(input_list), expected_output)

    def test_only_nested_lists(self):
        input_list = [[[], []], [[]]]
        expected_output = []
        self.assertEqual(questions.list_flatten(input_list), expected_output)

    def test_single_nested_list(self):
        input_list = [[1, 2, [3, 4]], 5]
        expected_output = [1, 2, 3, 4, 5]
        self.assertEqual(questions.list_flatten(input_list), expected_output)

class TestStrCompression(unittest.TestCase):
    """
    2 Katas
    """

    def test_single_occurrences(self):
        """Test a string with single occurrences of each character."""
        self.assertEqual(questions.str_compression('abc'), ['a', 'b', 'c'])

    def test_repeated_characters(self):
        """Test a string with repeated characters."""
        self.assertEqual(questions.str_compression('aaabbbccc'), ['a', 3, 'b', 3, 'c', 3])

    def test_mixed_single_and_repeated_characters(self):
        """Test a string with a mix of single and repeated characters."""
        self.assertEqual(questions.str_compression('aabcc'), ['a', 2, 'b', 'c', 2])

    def test_empty_string(self):
        """Test an empty string."""
        self.assertEqual(questions.str_compression(''), [])

    def test_non_alphabetic_characters(self):
        """Test a string with non-alphabetic characters, including digits and symbols."""
        self.assertEqual(questions.str_compression('1122!!a'), ['1', 2, '2', 2, '!', 2, 'a'])

    def test_single_character_repeated(self):
        """Test a string that is a single character repeated."""
        self.assertEqual(questions.str_compression('aaaa'), ['a', 4])

    def test_single_character(self):
        """Test a string that is a single character."""
        self.assertEqual(questions.str_compression('a'), ['a'])

    def test_case_sensitivity(self):
        """Test that the function is case-sensitive."""
        self.assertEqual(questions.str_compression('aAaA'), ['a', 'A', 'a', 'A'])

class TestStrongPass(unittest.TestCase):
    """
    1 Katas
    """

    def test_short_password(self):
        """Test that a short password is considered not strong."""
        self.assertFalse(questions.strong_pass('Aa!2'))

    def test_no_digit(self):
        """Test that a password without a digit is considered not strong."""
        self.assertFalse(questions.strong_pass('Abcdef!'))

    def test_no_lowercase(self):
        """Test that a password without a lowercase letter is considered not strong."""
        self.assertFalse(questions.strong_pass('ABCDEF1!'))

    def test_no_uppercase(self):
        """Test that a password without an uppercase letter is considered not strong."""
        self.assertFalse(questions.strong_pass('abcdef1!'))

    def test_no_special_character(self):
        """Test that a password without a special character is considered not strong."""
        self.assertFalse(questions.strong_pass('Abcdef1'))

    def test_strong_password(self):
        """Test that a valid password is considered strong."""
        self.assertTrue(questions.strong_pass('Aa!2bcD'))



if __name__ == '__main__':
    import inspect
    import sys
    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))
