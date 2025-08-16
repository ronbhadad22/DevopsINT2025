import os
import io
import tarfile
import shutil
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from unittest.mock import patch
import atexit

# Ensure we can import utils.py (one level up)
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import unittest_runner
import kata_questions_2 as questions

# ---------- Universal PASS/FAIL summary (works with PyCharm runner too) ----------
_original_run = unittest.TestCase.run
_test_outcomes = []  # list of (STATUS, test_id)

def _tracking_run(self, result=None):
    ret = _original_run(self, result)
    try:
        if result is not None:
            tid = self.id()
            if any(t.id() == tid for t, _ in getattr(result, 'failures', [])):
                status = 'FAIL'
            elif any(t.id() == tid for t, _ in getattr(result, 'errors', [])):
                status = 'ERROR'
            elif any(t.id() == tid for t, _ in getattr(result, 'skipped', [])):
                status = 'SKIPPED'
            elif any(t.id() == tid for t, _ in getattr(result, 'expectedFailures', [])):
                status = 'XFAIL'
            elif any(t.id() == tid for t in getattr(result, 'unexpectedSuccesses', [])):
                status = 'XPASS'
            else:
                status = 'PASS'
            _test_outcomes.append((status, tid))
    except Exception:
        # Don't interfere with test execution if our summary logic fails
        pass
    return ret

unittest.TestCase.run = _tracking_run

@atexit.register
def _print_summary():
    if not _test_outcomes:
        return
    print("\n================ Test Outcome Summary ================")
    # group by status to make it easy to skim
    order = ['PASS', 'FAIL', 'ERROR', 'SKIPPED', 'XFAIL', 'XPASS']
    grouped = {k: [] for k in order}
    for status, tid in _test_outcomes:
        grouped.setdefault(status, []).append(tid)
    for status in order:
        tests = grouped.get(status) or []
        if tests:
            print(f"\n{status} ({len(tests)})")
            for t in tests:
                print(f"  - {t}")
    print("======================================================\n")
# -------------------------------------------------------------------------------


class TestValidParentheses(unittest.TestCase):
    """3 Kata"""
    def test_examples(self):
        self.assertTrue(questions.valid_parentheses('[[{()}](){}]'))
        self.assertFalse(questions.valid_parentheses(']}'))
        self.assertTrue(questions.valid_parentheses('()[]{}'))
        self.assertFalse(questions.valid_parentheses('([)]'))
        self.assertTrue(questions.valid_parentheses(''))

    def test_single_types(self):
        self.assertTrue(questions.valid_parentheses('()'))
        self.assertTrue(questions.valid_parentheses('[]'))
        self.assertTrue(questions.valid_parentheses('{}'))
        self.assertFalse(questions.valid_parentheses('('))
        self.assertFalse(questions.valid_parentheses(']'))


class TestFibonacciFixme(unittest.TestCase):
    """2 Kata"""
    def test_small(self):
        for n, exp in [(1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (10, 55), (0, 0), (-5, 0)]:
            self.assertEqual(questions.fibonacci_fixme(n), exp)


class TestMostFrequentName(unittest.TestCase):
    """2 Kata"""
    def setUp(self):
        self.file_path = 'names.txt'
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write('alice\nbob\nalice\ncarol\n')

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_basic(self):
        self.assertEqual(questions.most_frequent_name(self.file_path), 'alice')

    def test_tie(self):
        path = 'names_tie.txt'
        with open(path, 'w', encoding='utf-8') as f:
            f.write('a\nb\na\nb\n')
        try:
            self.assertIn(questions.most_frequent_name(path), {'a', 'b'})
        finally:
            if os.path.exists(path):
                os.remove(path)


class TestFilesBackup(unittest.TestCase):
    """3 Kata"""
    def setUp(self):
        self.dir_path = 'temp_files_to_backup_unittest'
        os.makedirs(self.dir_path, exist_ok=True)
        with open(os.path.join(self.dir_path, 'a.txt'), 'w') as f:
            f.write('A')
        with open(os.path.join(self.dir_path, 'b.txt'), 'w') as f:
            f.write('B')

    def tearDown(self):
        shutil.rmtree(self.dir_path, ignore_errors=True)
        date_str = datetime.now().strftime('%Y-%m-%d')
        archive_name = f"backup_{os.path.basename(self.dir_path)}_{date_str}.tar.gz"
        if os.path.exists(archive_name):
            os.remove(archive_name)

    def test_backup_archive_created(self):
        archive_name = questions.files_backup(self.dir_path)
        self.assertTrue(os.path.exists(archive_name))
        self.assertTrue(tarfile.is_tarfile(archive_name))
        with tarfile.open(archive_name, 'r:gz') as tar:
            members = [m.name for m in tar.getmembers() if m.isfile()]
        self.assertTrue(any(name.endswith('a.txt') for name in members))
        self.assertTrue(any(name.endswith('b.txt') for name in members))


class TestReplaceInFile(unittest.TestCase):
    """2 Kata"""
    def setUp(self):
        self.file_path = 'temp.yaml'
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write('image: {{IMG_NAME}}\n')

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_replace(self):
        questions.replace_in_file(self.file_path, '{{IMG_NAME}}', 'mnist-pred:0.0.1')
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('mnist-pred:0.0.1', content)
        self.assertNotIn('{{IMG_NAME}}', content)


class TestJsonConfigsMerge(unittest.TestCase):
    """2 Kata"""
    def setUp(self):
        self.default = 'default.json'
        self.local = 'local.json'
        with open(self.default, 'w', encoding='utf-8') as f:
            f.write('{"a": 1, "b": 2}')
        with open(self.local, 'w', encoding='utf-8') as f:
            f.write('{"b": 3, "c": 4}')

    def tearDown(self):
        for p in [self.default, self.local]:
            if os.path.exists(p):
                os.remove(p)

    def test_merge(self):
        merged = questions.json_configs_merge(self.default, self.local)
        self.assertEqual(merged, {"a": 1, "b": 3, "c": 4})


class TestMonotonicArray(unittest.TestCase):
    """1 Kata"""
    def test_cases(self):
        self.assertTrue(questions.monotonic_array([1, 2, 2, 3]))
        self.assertTrue(questions.monotonic_array([3, 2, 2, 1]))
        self.assertFalse(questions.monotonic_array([1, 3, 2]))
        self.assertTrue(questions.monotonic_array([]))
        self.assertTrue(questions.monotonic_array([5]))


class TestMatrixAvg(unittest.TestCase):
    """2 Kata"""
    def test_all_rows(self):
        mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(questions.matrix_avg(mat), 5)

    def test_some_rows(self):
        mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(questions.matrix_avg(mat, rows=[0, 2]), 5)

    def test_empty_rows(self):
        mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(questions.matrix_avg(mat, rows=[]), 0)


class TestMergeSortedLists(unittest.TestCase):
    """1 Kata"""
    def test_merge(self):
        self.assertEqual(
            questions.merge_sorted_lists([1, 4, 9, 77, 13343], [-7, 0, 7, 23]),
            [-7, 0, 1, 4, 7, 9, 23, 77, 13343]
        )

    def test_merge_edge(self):
        self.assertEqual(questions.merge_sorted_lists([], [1, 2]), [1, 2])
        self.assertEqual(questions.merge_sorted_lists([1, 2], []), [1, 2])
        self.assertEqual(questions.merge_sorted_lists([], []), [])


class TestLongestCommonSubstring(unittest.TestCase):
    """4 Kata"""
    def test_basic(self):
        self.assertEqual(questions.longest_common_substring('abcdefg', 'bgtcdesd'), 'cde')
        self.assertEqual(questions.longest_common_substring('', 'abc'), '')
        self.assertEqual(questions.longest_common_substring('abc', ''), '')


class TestLongestCommonPrefix(unittest.TestCase):
    """1 Kata"""
    def test_basic(self):
        self.assertEqual(questions.longest_common_prefix('abcd', 'abxy'), 'ab')
        self.assertEqual(questions.longest_common_prefix('abcd', 'ttty'), '')


class TestRotateMatrix(unittest.TestCase):
    """2 Kata"""
    def test_rotate(self):
        mat = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
        expected = [[6, 1], [7, 2], [8, 3], [9, 4], [10, 5]]
        self.assertEqual(questions.rotate_matrix(mat), expected)

    def test_rotate_empty(self):
        self.assertEqual(questions.rotate_matrix([]), [])


class TestIsValidEmail(unittest.TestCase):
    """3 Kata"""
    @patch('kata_questions_2.socket.gethostbyname', return_value='1.2.3.4')
    def test_basic(self, _):
        self.assertTrue(questions.is_valid_email('example@gmail.com'))
        self.assertFalse(questions.is_valid_email('!bad@domain.com'))
        self.assertFalse(questions.is_valid_email('nodomain'))
        self.assertFalse(questions.is_valid_email('@nodomain'))
        self.assertFalse(questions.is_valid_email('user@'))

    def test_dns_fail(self):
        with patch('kata_questions_2.socket.gethostbyname', side_effect=OSError):
            self.assertFalse(questions.is_valid_email('user@nonexistent.invalidtld'))


class TestPascalTriangle(unittest.TestCase):
    """3 Kata"""
    def test_print(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            questions.pascal_triangle(5)
            output = buf.getvalue().strip().splitlines()
        self.assertEqual(output[0], '1')
        self.assertEqual(output[1], '1 1')
        self.assertEqual(output[2], '1 2 1')

    def test_zero(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            questions.pascal_triangle(0)
            output = buf.getvalue().strip()
        self.assertEqual(output, '')


class TestListFlatten(unittest.TestCase):
    """2 Kata"""
    def test_nested(self):
        data = [1, [], [1, 2, [4, 0, [5], 6], [5, 4], 34, 0], [3]]
        expected = [1, 1, 2, 4, 0, 5, 6, 5, 4, 34, 0, 3]
        self.assertEqual(questions.list_flatten(data), expected)

    def test_already_flat(self):
        self.assertEqual(questions.list_flatten([1, 2, 3]), [1, 2, 3])


class TestStrCompression(unittest.TestCase):
    """2 Kata"""
    def _decode(self, compressed):
        out = []
        i = 0
        while i < len(compressed):
            ch = compressed[i]
            cnt = 1
            if i + 1 < len(compressed) and isinstance(compressed[i + 1], int):
                cnt = compressed[i + 1]
                i += 2
            else:
                i += 1
            out.append(ch * cnt)
        return ''.join(out)

    def test_compress(self):
        text = 'aaaaabbcaasbbgvccf'
        compressed = questions.str_compression(text)
        self.assertEqual(self._decode(compressed), text)

    def test_empty(self):
        self.assertEqual(questions.str_compression(''), [])


class TestStrongPass(unittest.TestCase):
    """1 Kata"""
    def test_strength(self):
        self.assertTrue(questions.strong_pass('##$FgC7^^5a'))
        self.assertFalse(questions.strong_pass('short'))
        self.assertFalse(questions.strong_pass('NoSpecial7'))
        self.assertFalse(questions.strong_pass('nospecial7a'))
        self.assertFalse(questions.strong_pass('NOSPECIAL7A'))


if __name__ == "__main__":
    unittest_runner([
        ("TestValidParentheses", TestValidParentheses),
        ("TestFibonacciFixme", TestFibonacciFixme),
        ("TestMostFrequentName", TestMostFrequentName),
        ("TestFilesBackup", TestFilesBackup),
        ("TestReplaceInFile", TestReplaceInFile),
        ("TestJsonConfigsMerge", TestJsonConfigsMerge),
        ("TestMonotonicArray", TestMonotonicArray),
        ("TestMatrixAvg", TestMatrixAvg),
        ("TestMergeSortedLists", TestMergeSortedLists),
        ("TestLongestCommonSubstring", TestLongestCommonSubstring),
        ("TestLongestCommonPrefix", TestLongestCommonPrefix),
        ("TestRotateMatrix", TestRotateMatrix),
        ("TestIsValidEmail", TestIsValidEmail),
        ("TestPascalTriangle", TestPascalTriangle),
        ("TestListFlatten", TestListFlatten),
        ("TestStrCompression", TestStrCompression),
        ("TestStrongPass", TestStrongPass),
    ])
