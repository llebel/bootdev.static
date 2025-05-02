from textnode import TextNode, TextType


def main():
    testNode = TextNode("Hello World", TextType.NORMAL, "https://example.com")
    print(testNode)

if __name__ == "__main__":
    main()
