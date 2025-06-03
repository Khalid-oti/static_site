import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    #HTMLNode
    def test_eq(self):
        node = HTMLNode(tag="h1", value="random text")
        node2 = HTMLNode(tag="h1", value="random text")
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = HTMLNode(value="random text")
        node2 = HTMLNode(tag="h1", value="random text")
        self.assertNotEqual(node, node2)
    def test_children_props(self):
        node = HTMLNode(children=["node3", "node4"], props={"href": "https://www.google.com"})
        node2 = HTMLNode(props={"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)
    #LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_prop(self):
        node = LeafNode("a", "hello there", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">hello there</a>')
    def test_no_tag(self):
        node = LeafNode(None, "Hey there world")
        self.assertEqual(node.to_html(), "Hey there world")
    def test_leaf_to_html_i(self):
        node = LeafNode("i", "leaning tower")
        self.assertEqual(node.to_html(), "<i>leaning tower</i>")
    #ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")


if __name__ == "__main__":
    unittest.main()