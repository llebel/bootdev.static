import re
from textnode import TextNode, TextType, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGES,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text: str) -> list[TextNode]:
    if not text:
        return TextNode("", TextType.TEXT)
    
    result = TextNode(text, TextType.TEXT)
    result = split_nodes_delimiter([result], "`", TextType.CODE)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    result = [node for node in result if node.text or node.text_type != TextType.TEXT]
    return result    

def markdown_to_blocks(markdown: str) -> list[str]:
    if not markdown:
        return []
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        blocks.append(block)
    return blocks

def is_ordered_list(block: str) -> bool:
    pattern = r"^(\d+)\. "
    for counter, line in enumerate(block.split("\n"), start=1):
        match = re.match(pattern, line)
        if not match or int(match.group(1)) != counter:
            return False
    return True
    
def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^[#]{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    
    for text_node in text_nodes:
        node = text_node_to_html_node(text_node)
        html_nodes.append(node)

    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def overwrite_public_files(source_dir, dest_dir):
    import os
    import shutil

    # Cleanup destination directory
    if os.path.exists(dest_dir):
        print(f"Cleaning up destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.makedirs(dest_dir, exist_ok=True)

    # Copy files from source to destination
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        dest_file = os.path.join(dest_dir, filename)

        if os.path.isfile(source_file):
            print(f"Copying file: {source_file} to {dest_file}")
            shutil.copy2(source_file, dest_file)
        elif os.path.isdir(source_file):
            print(f"Copying directory: {source_file} to {dest_file}")
            shutil.copytree(source_file, dest_file, dirs_exist_ok=True)

def extract_title(markdown):
    """
    Extract the title from the markdown content.
    The title is assumed to be the first line of the markdown.
    """
    if not markdown:
        raise ValueError("Markdown content is empty")
    first_line = markdown.split("\n")[0].strip()
    if first_line.startswith("#"):
        return first_line.lstrip("#").strip()
    raise ValueError("Title not found in markdown content")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")

    import os
    with open(from_path, 'r', encoding='utf-8') as f:
        print(f"Reading markdown content from {from_path}")
        if not os.path.exists(from_path):
            raise FileNotFoundError(f"Markdown file {from_path} does not exist")
        markdown_content = f.read()

    with open(template_path, 'r', encoding='utf-8') as f:
        print(f"Reading template content from {template_path}")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file {template_path} does not exist")
        template_content = f.read()

    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    html_content = template_content.replace("{{ Content }}", html_string).replace("{{ Title }}", title)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    import os

    if not os.path.exists(content_dir_path):
        raise FileNotFoundError(f"Content directory {content_dir_path} does not exist")

    for root, dirs, files in os.walk(content_dir_path):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, content_dir_path)
                dest_path = os.path.join(dest_dir_path, relative_path.replace(".md", ".html"))
                print(f"Generating page for {from_path} to {dest_path}")
                generate_page(from_path, template_path, dest_path)
    print(f"All pages generated in {dest_dir_path}")
