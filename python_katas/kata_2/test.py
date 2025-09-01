import os
import io
import shutil
import unittest
from contextlib import redirect_stdout

from python_katas.kata_2 import questions


class TestValidParentheses(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(questions.valid_parentheses("()[]{}"))
        self.assertTrue(questions.valid_parentheses("[{()}](){}"))

    def test_invalid(self):
        self.assertFalse(questions.valid_parentheses("(]"))
        self.assertFalse(questions.valid_parentheses("([)]"))
        self.assertFalse(questions.valid_parentheses("]}"))


class TestFibonacciFixme(unittest.TestCase):
    def test_values(self):
        self.assertEqual(questions.fibonacci_fixme(1), 1)
        self.assertEqual(questions.fibonacci_fixme(2), 1)
        self.assertEqual(questions.fibonacci_fixme(3), 2)
        self.assertEqual(questions.fibonacci_fixme(6), 8)


class TestMostFrequentName(unittest.TestCase):
    def setUp(self):
        with open("names.txt", "w") as f:
            f.write("roee\nroee\ndavid\ntal\n")

    def tearDown(self):
        os.remove("names.txt")

    def test_most_frequent(self):
        self.assertEqual(questions.most_frequent_name("names.txt"), "roee")


class TestFilesBackup(unittest.TestCase):
    def setUp(self):
        os.mkdir("files_to_backup")
        with open("files_to_backup/file1.txt", "w") as f:
            f.write("hello")

    def tearDown(self):
        shutil.rmtree("files_to_backup")
        for f in os.listdir():
            if f.startswith("backup_files_to_backup_") and f.endswith(".tar.gz"):
                os.remove(f)

    def test_backup(self):
        fname = questions.files_backup("files_to_backup")
        self.assertTrue(os.path.exists(fname))
        self.assertTrue(fname.endswith(".tar.gz"))


class TestReplaceInFile(unittest.TestCase):
    def setUp(self):
        with open("tmp.txt", "w") as f:
            f.write("Hello {{NAME}}")

    def tearDown(self):
        os.remove("tmp.txt")

    def test_replace(self):
        questions.replace_in_file("tmp.txt", "{{NAME}}", "Tal")
        with open("tmp.txt") as f:
            self.assertIn("Tal", f.read())


class TestJsonConfigsMerge(unittest.TestCase):
    def setUp(self):
        with open("a.json", "w") as f:
            f.write('{"x": 1, "y": 2}')
        with open("b.json", "w") as f:
            f.write('{"y": 3, "z": 4}')

    def tearDown(self):
        os.remove("a.json")
        os.remove("b.json")

    def test_merge(self):
        res = questions.json_configs_merge("a.json", "b.json")
        self.assertEqual(res["x"], 1)
        self.assertEqual(res["y"], 3)
        self.assertEqual(res["z"], 4)


class TestMonotonicArray(unittest.TestCase):
    def test_inc(self):
        self.assertTrue(questions.monotonic_array([1, 2, 3, 4]))
    def test_dec(self):
        self.assertTrue(questions.monotonic_array([5, 4, 3, 1]))
    def test_not(self):
        self.assertFalse(questions.monotonic_array([1, 3, 2]))


class TestMatrixAvg(unittest.TestCase):
    def test_all(self):
        mat = [[1,2,3],[4,5,6],[7,8,9]]
        self.assertEqual(questions.matrix_avg(mat), 5)
    def test_rows(self):
        mat = [[1,2,3],[4,5,6],[7,8,9]]
        self.assertEqual(questions.matrix_avg(mat, rows=[0,2]), 5)


class TestMergeSortedLists(unittest.TestCase):
    def test_merge(self):
        self.assertEqual(
            questions.merge_sorted_lists([1,3,5], [2,4,6]),
            [1,2,3,4,5,6]
        )


class TestLongestCommonSubstring(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            questions.longest_common_substring("abcdef", "zabcf"),
            "abc"
        )
    def test_none(self):
        self.assertEqual(
            questions.longest_common_substring("abc", "xyz"), ""
        )


class TestLongestCommonPrefix(unittest.TestCase):
    def test_prefix(self):
        self.assertEqual(
            questions.longest_common_prefix("hello world", "hello tal"),
            "hello "
        )
    def test_none(self):
        self.assertEqual(
            questions.longest_common_prefix("abc", "xyz"),
            ""
        )


class TestRotateMatrix(unittest.TestCase):
    def test_rotate(self):
        mat = [[1,2,3],[4,5,6]]
        self.assertEqual(questions.rotate_matrix(mat), [[4,1],[5,2],[6,3]])


class TestIsValidEmail(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(questions.is_valid_email("gmail.com@gmail.com"))
    def test_invalid(self):
        self.assertFalse(questions.is_valid_email("bad@@gmail.com"))
        self.assertFalse(questions.is_valid_email("noatsign.com"))


class TestPascalTriangle(unittest.TestCase):
    def test_output(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            questions.pascal_triangle(3)
        out = buf.getvalue().strip()
        self.assertIn("1 2 1", out)


class TestListFlatten(unittest.TestCase):
    def test_flat(self):
        self.assertEqual(
            questions.list_flatten([1,[2,[3]],4]),
            [1,2,3,4]
        )


class TestStrCompression(unittest.TestCase):
    def test_compression(self):
        self.assertEqual(
            questions.str_compression("aaaabbc"),
            ["a",4,"b",2,"c"]
        )


class TestStrongPass(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(questions.strong_pass("Abc$12"))
    def test_invalid(self):
        self.assertFalse(questions.strong_pass("abc"))
