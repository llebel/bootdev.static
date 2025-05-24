from textnode import TextNode, TextType
from utils import overwrite_public_files, generate_page, generate_pages_recursive


def main():
    testNode = TextNode("Hello World", TextType.TEXT, "https://example.com")
    print(testNode)

    # Overwrite public files from static to public directory
    overwrite_public_files("static", "public")

    # Generate HTML from text nodes
    # generate_page("content/index.md", "template.html", "public/index.html")
    
    # Generate HTML pages recursively from a directory
    generate_pages_recursive("content", "template.html", "public")

    print("HTML pages generated successfully.")


if __name__ == "__main__":
    main()
