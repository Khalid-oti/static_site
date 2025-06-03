import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes


class TestTextNode(unittest.TestCase):
    #TextNode
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("text", TextType.BOLD, url="mbc.net")
        node2 = TextNode("text", TextType.BOLD)
        self.assertNotEqual(node, node2)
    #Textnode to HTMLNode
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "github.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "github.com"})
    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "wikipedia.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "wikipedia.org", "alt": "This is a text node"})
    #Markdown to TextNode
    def test_md_to_code(self):
        node = TextNode("words...`code`words...", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_node[0], TextNode("words...", TextType.TEXT))
        self.assertEqual(new_node[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_node[2], TextNode("words...", TextType.TEXT))
    def test_md_to_bold(self):
        node = TextNode("words...**bold**words...", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_node[0], TextNode("words...", TextType.TEXT))
        self.assertEqual(new_node[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_node[2], TextNode("words...", TextType.TEXT))
    def test_md_to_italic(self):
        node = TextNode("words..._italic_words...", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_node[0], TextNode("words...", TextType.TEXT))
        self.assertEqual(new_node[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_node[2], TextNode("words...", TextType.TEXT))
    #links and images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("text", "https://i.imgur.com/zjjcJKZ.png")], matches)
    #images and links from markdown to text nodes
    def test_split_image_to_node(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_node = split_nodes_image([node])
        print(new_node[0])
        self.assertEqual(new_node[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_node[1], TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
    def test_split_link_to_node(self):
        node = TextNode("This is text with a [link](https://neal.fun)", TextType.TEXT)
        new_node = split_nodes_link([node])
        self.assertEqual(new_node[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_node[1], TextNode("link", TextType.LINK, "https://neal.fun"))
    #text to text node
    def test_text_to_text_node(self):
        text = "This **text** is long because it _utilizes_ all `markdown` types, here's an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://neal.fun)"
        text_to_node = text_to_text_nodes(text)
        self.assertEqual(text_to_node[0], TextNode("This ", TextType.TEXT))
        self.assertEqual(text_to_node[1], TextNode("text", TextType.BOLD))
        self.assertEqual(text_to_node[2], TextNode(" is long because it ", TextType.TEXT))
        self.assertEqual(text_to_node[3], TextNode("utilizes", TextType.ITALIC))
        self.assertEqual(text_to_node[4], TextNode(" all ", TextType.TEXT))
        self.assertEqual(text_to_node[5], TextNode("markdown", TextType.CODE))
        self.assertEqual(text_to_node[6], TextNode(" types, here's an ", TextType.TEXT))
        self.assertEqual(text_to_node[7], TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"))
        self.assertEqual(text_to_node[8], TextNode(" and a ", TextType.TEXT))
        self.assertEqual(text_to_node[9], TextNode("link", TextType.LINK, "https://neal.fun"))


if __name__ == "__main__":
    unittest.main()
