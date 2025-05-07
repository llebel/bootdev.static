import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        chunks = node.text.split(delimiter)
        odd = True
        for chunk in chunks:
            if chunk:
                if odd:
                    new_nodes.append(TextNode(chunk, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(chunk, text_type))
                odd = not odd

    return new_nodes

def extract_markdown_images(text):
    images = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        alt_text = match[0]
        url = match[1]
        images.append((alt_text, url))
    return images

def extract_markdown_links(text):
    links = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    for match in matches:
        link_text = match[0]
        url = match[1]
        links.append((link_text, url))
    return links
        