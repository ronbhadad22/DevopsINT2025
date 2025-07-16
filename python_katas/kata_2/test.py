import os
import unittest
import shutil
import tarfile
import io
from contextlib import redirect_stdout
from datetime import datetime
from python_katas.kata_2 import questions
from python_katas.utils import unittest_runner

testers = ['roee', 'david', 'tal gold']

class TestValidParentheses(unittest.TestCase):
    """
    3 Katas
    """

class TestFibonacciFixme(unittest.TestCase):
    """
    2 Katas
    """

class TestMostFrequentName(unittest.TestCase):
    """
    2 Katas
    """

class TestFilesBackup(unittest.TestCase):
    """
    3 Katas
    """

class TestReplaceInFile(unittest.TestCase):
    """
    2 Katas
    """

class TestJsonConfigsMerge(unittest.TestCase):
    """
    2 Katas
    """

class TestMonotonicArray(unittest.TestCase):
    """
    1 Katas
        """

class TestMatrixAvg(unittest.TestCase):
    """
    2 Katas
    """

class TestMergeSortedLists(unittest.TestCase):
    """
    1 Katas
    """

class TestLongestCommonSubstring(unittest.TestCase):
    """
    4 Katas
    """

class TestLongestCommonPrefix(unittest.TestCase):
    """
    1 Katas
    """


class TestRotateMatrix(unittest.TestCase):
    """
    2 Katas
    """

class TestIsValidEmail(unittest.TestCase):
    """
    3 Katas
    """

class TestPascalTriangle(unittest.TestCase):
    """
     3 Katas
     """


class TestListFlatten(unittest.TestCase):
    """
    2 Katas
    """

class TestStrCompression(unittest.TestCase):
    """
    2 Katas
    """

class TestStrongPass(unittest.TestCase):
    """
    1 Katas
    """



if __name__ == '__main__':
    import inspect
    import sys
    unittest_runner(inspect.getmembers(sys.modules[__name__], inspect.isclass))
