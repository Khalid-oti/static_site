import unittest
from markdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestMarkdown(unittest.TestCase):
    #Markdown to blocks tests
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    #block type tests
    def test_block_to_block_type_ordered_list(self):
        block = "1. Always Win Your Battles" \
        "2. Never Let Them Laugh at You" \
        "3. Always Be Rested"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED)
    def test_block_to_block_type_code(self):
        block = "```" \
        "if this then that else that" \
        "variables and functions" \
        "```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    def test_block_to_block_type_paragraph(self):
        block = "normal text" \
        "nothing to see here" \
        "just a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_block_to_block_type_heading(self):
        block = "### look at this heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    #Block to HTML
    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """
    
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )