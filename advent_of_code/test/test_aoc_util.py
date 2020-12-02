from unittest import TestCase
from util import aoc_util


class Test(TestCase):

    def test_tokenize(self):
        text = '1-3 a: abcde'
        tokens = aoc_util.tokenize(text, '- :')
        self.assertEqual(tokens, [1, 3, 'a', 'abcde'])

        text = ''
        tokens = aoc_util.tokenize(text)
        self.assertEqual(tokens, [])

        text = ' a b c '
        tokens = aoc_util.tokenize(text)
        self.assertEqual(tokens, ['a', 'b', 'c'])

        text = 'a b c'
        tokens = aoc_util.tokenize(text)
        self.assertEqual(tokens, ['a', 'b', 'c'])

        text = 'a  b  c'
        tokens = aoc_util.tokenize(text)
        self.assertEqual(tokens, ['a', 'b', 'c'])

        text = 'a \t b \t c'
        tokens = aoc_util.tokenize(text)
        self.assertEqual(tokens, ['a', 'b', 'c'])

        text = 'word 42 123.456'
        tokens = aoc_util.tokenize(text)
        self.assertEqual(tokens, ['word', 42, 123.456])
