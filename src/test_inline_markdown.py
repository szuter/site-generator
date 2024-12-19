import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)


from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_text(self):
        node = TextNode("This is text without a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text without a code block word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_raise(self):
        node = TextNode("This is text with a code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delim_empty_string(self):
        node = TextNode("Hello `code` `another`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("another", TextType.CODE),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

        def test_split_nodes_image_single(self):
            node = TextNode(
                "Hello ![image](https://example.com/img.png) world", TextType.TEXT
            )
            self.assertListEqual(
                split_nodes_image([node]),
                [
                    TextNode("Hello ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                    TextNode(" world", TextType.TEXT),
                ],
            )

    def test_split_nodes_image_empty_string(self):
        node = TextNode("", TextType.TEXT)
        nodes = split_nodes_image([node])
        assert len(nodes) == 0

    def test_split_nodes_link_no_links(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text without a link", TextType.TEXT),
            ],
        )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        self.assertListEqual(
            split_nodes_image([node]),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_split_nodes_link_single(self):
        node = TextNode("[Click me](https://boot.dev)", TextType.TEXT)
        self.assertListEqual(
            split_nodes_link([node]),
            [
                TextNode("Click me", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_split_nodes_link_invalid(self):
        node = [
            TextNode("This has [link](unclosed", TextType.TEXT),
            TextNode("This has [link]unclosed)", TextType.TEXT),
            TextNode("This has [link(unclosed)", TextType.TEXT),
            TextNode("This has link[(unclosed)", TextType.TEXT),
        ]
        with self.assertRaises(ValueError):
            split_nodes_link(node)

    def test_split_nodes_link_empty_text(self):
        node = TextNode("This has []()", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_link([node])

    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_bold_in_link(self):
        text = "Click this [**bold** link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Click this ", TextType.TEXT),
                TextNode("**bold** link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
