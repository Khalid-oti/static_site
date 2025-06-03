import unittest

from main import extract_title

class TestMainFuncs(unittest.TestCase):
    def test_extract_h1(self):
        md = """
            # title
            words and more words
            this part doesn't matter
        """

        self.assertEqual(extract_title(md), "title")