import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter

class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        # Test splitting a text node with a delimiter
        nodes = [TextNode("Hello, World!", TextType.TEXT)]
        delimiter = ", "
        text_type = TextType.BOLD
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Hello")
        self.assertEqual(result[1].text, "World!")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result, expected)
