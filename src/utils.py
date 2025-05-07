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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Just pass through non-text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Now handle TEXT node
        text = node.text
        if not text:
            continue
        # Split the text by images
        parts = re.split(r"!\[(.*?)\]\((.*?)\)", text)
        for i in range(0, len(parts), 3):
            # Add the text part
            if i < len(parts):
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            # Add the image part
            if i + 1 < len(parts) and i + 2 < len(parts):
                new_nodes.append(TextNode(parts[i + 1], TextType.IMAGES, parts[i + 2]))
        # If there is a trailing text part, add it
        if len(parts) % 3 == 1:
            new_nodes.append(TextNode(parts[-1], TextType.TEXT))
        elif len(parts) % 3 == 2:
            new_nodes.append(TextNode(parts[-2], TextType.TEXT))
            new_nodes.append(TextNode(parts[-1], TextType.IMAGES, None))
    # Remove empty nodes
    new_nodes = [node for node in new_nodes if node.text or node.text_type != TextType.TEXT]
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Just pass through non-text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Now handle TEXT node
        text = node.text
        if not text:
            continue
        # Split the text by links
        parts = re.split(r"\[(.*?)\]\((.*?)\)", text)
        for i in range(0, len(parts), 3):
            # Add the text part
            if i < len(parts):
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            # Add the link part
            if i + 1 < len(parts) and i + 2 < len(parts):
                new_nodes.append(TextNode(parts[i + 1], TextType.LINKS, parts[i + 2]))
        # If there is a trailing text part, add it
        if len(parts) % 3 == 1:
            new_nodes.append(TextNode(parts[-1], TextType.TEXT))
        elif len(parts) % 3 == 2:
            new_nodes.append(TextNode(parts[-2], TextType.TEXT))
            new_nodes.append(TextNode(parts[-1], TextType.LINKS, None))

    # Remove empty nodes
    new_nodes = [node for node in new_nodes if node.text or node.text_type != TextType.TEXT]
            
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
        