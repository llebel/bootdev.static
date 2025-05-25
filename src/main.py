
from textnode import TextNode, TextType
from utils import overwrite_public_files, generate_page, generate_pages_recursive


def main():
    import sys

    if len(sys.argv) != 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    

    # Overwrite public files from static to public directory
    overwrite_public_files("static", "docs")

    # Generate HTML from text nodes
    # generate_page("content/index.md", "template.html", "public/index.html", basepath)
    
    # Generate HTML pages recursively from a directory
    generate_pages_recursive("content", "template.html", "docs", basepath)

    print("HTML pages generated successfully.")


if __name__ == "__main__":
    main()
