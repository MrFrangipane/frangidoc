import unittest
from frangidoc import parser as p
from .data import *


class Test(unittest.TestCase):

    def test_1_empty_file(self):
        parser = p.Parser([])
        result = parser.parse()

        self.assertEqual(result, None)

    def test_2_only_blank_lines(self):
        parser = p.Parser(['', '', ''])
        result = parser.parse()

        self.assertEqual(result, None)

    def test_3_only_docstring(self):
        parser = p.Parser(DOCSTRING.splitlines())
        result = parser.parse()

    def test_4_classes(self):
        for class_text in CLASSES:
            print('-' * 50 + '\n' + class_text + '\n\n')
            parser = p.Parser(class_text.splitlines())
            print(parser.parse())
