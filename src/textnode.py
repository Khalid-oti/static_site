from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold" #**
    ITALIC = "Italic" #_
    CODE = "Code" #`
    LINK = "Link" #[
    IMAGE = "Image" #![

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_node = []
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid Markdown syntax")
            split_node = node.text.split(delimiter)
            for i in range(len(split_node)):
                if split_node[i] == "":
                    continue
                if i % 2 == 0:
                    new_node.append(TextNode(split_node[i], TextType.TEXT))
                if i % 2 == 1:
                    new_node.append(TextNode(split_node[i], text_type))
            new_nodes.extend(new_node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def shared_split_node_code(old_nodes, delimiter, text_type, extract_func):
    new_nodes = []
    for node in old_nodes:
        og_text = node.text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_node = []
            images_links = extract_func(og_text)
            if len(images_links) == 0:
                new_nodes.append(node)
                continue
            for image_link in images_links:
                split_node = og_text.split(f"{delimiter}{image_link[0]}]({image_link[1]})", 1)
                if len(split_node) != 2:
                    raise Exception("Invalid markdown")
                if split_node[0] != "":
                    new_node.append(TextNode(split_node[0], TextType.TEXT))
                new_node.append(TextNode(image_link[0], text_type, image_link[1]))
                og_text = split_node[1]
            if og_text != "":
                new_node.append(TextNode(og_text, TextType.TEXT))
            new_nodes.extend(new_node)
    return new_nodes

def split_nodes_image(old_nodes):
    return shared_split_node_code(old_nodes, "![", TextType.IMAGE, extract_markdown_images)

def split_nodes_link(old_nodes):
    return shared_split_node_code(old_nodes, "[", TextType.LINK, extract_markdown_links)

def text_to_text_nodes(text):
    return split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)],
                        "**", 
                        TextType.BOLD
                    ), 
                    "_", 
                    TextType.ITALIC
                ),
                "`",
                TextType.CODE
            )
        )
    )