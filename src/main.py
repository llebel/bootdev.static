from textnode import TextNode, TextType
from utils import overwrite_public_files


def main():
    testNode = TextNode("Hello World", TextType.TEXT, "https://example.com")
    print(testNode)

    overwrite_public_files("static", "public")

if __name__ == "__main__":
    main()
