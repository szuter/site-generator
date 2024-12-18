import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        child_node = HTMLNode("p", "text")
        node = HTMLNode("p", "text", child_node, self.props)

        self.assertEqual(
            "HTMLNode(p, text, children: HTMLNode(p, text, children: None, None), {'href': 'https://www.google.com', 'target': '_blank'})",
            repr(node),
        )

    def test_props_to_html(self):
        node = HTMLNode("p", "text", None, self.props)
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_none_props_to_html(self):
        node = HTMLNode("p", "text")
        self.assertEqual("", node.props_to_html())

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
