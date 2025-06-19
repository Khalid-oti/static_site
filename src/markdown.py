import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import text_node_to_html_node, text_to_text_nodes, TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED = "Unordered List"
    ORDERED = "Ordered List"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block.strip() == "":
            continue
        lines = block.split("\n")
        new_block = []
        for line in lines:
            if line.strip() == "":
                continue
            new_block.append(line.strip())
        new_blocks.append("\n".join(new_block))
    return new_blocks


def block_to_block_type(block):
    lines = block.split("\n")
    pound_count = 0
    quote_counter = 0
    unordered_counter = 0
    ordered_counter = 0

    for i in range(7):
        if block[i] == "#":
            pound_count += 1
        if block[i] == " ":
            if 0 < pound_count < 7:
                return BlockType.HEADING
            else:
                break

    if block[0:3] == "```":
        if block[-1:-4:-1] == "```":
            return BlockType.CODE 
        
    for line in lines:
        if line == "":
            continue
        if line[0] == ">":
            quote_counter += 1
        if line[0:2] == "- ":
            unordered_counter += 1
        if line[0:2+len(str(ordered_counter))] == f"{ordered_counter+1}. ":
            ordered_counter += 1
    if quote_counter == len(lines):
        return BlockType.QUOTE
    if unordered_counter == len(lines):
        return BlockType.UNORDERED
    if ordered_counter == len(lines):
        return BlockType.ORDERED
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_nodes.append(block_to_html_node(block))
    return ParentNode(tag="div", children=html_nodes, props=None)

def text_to_children(text):
    children = []
    text_nodes = text_to_text_nodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return markdown_to_paragraph(block)
    if block_type == BlockType.HEADING:
        return markdown_to_heading(block)
    if block_type == BlockType.CODE:
        return markdown_to_code(block)
    if block_type == BlockType.QUOTE:
        return markdown_to_quote(block)
    if block_type == BlockType.UNORDERED:
        return markdown_to_unordered(block)
    if block_type == BlockType.ORDERED:
        return markdown_to_ordered(block)

def markdown_to_paragraph(block):
    paragraph = ' '.join(block.split("\n"))
    return ParentNode(tag="p", children=text_to_children(paragraph), props=None)

def markdown_to_heading(block):
    pound_count = 0
    for char in block[:6]:
        if char == "#":
            pound_count += 1
        else:
            break
    return ParentNode(tag=f"h{pound_count}", children=text_to_children(block[pound_count+1:]), props=None)

def markdown_to_code(block):
    child_node = text_node_to_html_node(TextNode(block[3:-3].lstrip(), TextType.CODE))
    return ParentNode(tag="pre", children=[child_node], props=None)
    
def markdown_to_quote(block):
    text = block[1:]
    return ParentNode(tag="blockquote", children=text_to_children(text), props=None)
    
def markdown_to_unordered(block):
    new_block = []
    split_block = block.split("\n")
    for line in split_block:
        node = ParentNode(tag="li", children=text_to_children(line[2:]))
        new_block.append(node)
    return ParentNode(tag="ul", children=new_block, props=None)
    
def markdown_to_ordered(block):
    new_block = []
    split_block = block.split("\n")
    line_number = 0
    for line in split_block:
        line_number += 1
        text = line[2+len(str(line_number)):]
        node = ParentNode(tag="li", children=text_to_children(text))
        new_block.append(node)
    return ParentNode(tag="ol", children=new_block, props=None)