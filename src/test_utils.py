import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
