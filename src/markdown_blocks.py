from inline_markdown import text_to_textnodes
from htmlnode import ParentNode
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    block_lst = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        block_lst.append(block)
    return block_lst


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if line.startswith(">"):
                continue
            else:
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* ") or block.startswith("- "):
        char = lines[0][0] + lines[0][1]
        for line in lines:
            if not line.startswith(char):
                return block_type_paragraph
        return block_type_ulist

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph


def markdown_to_html_node(markdown):
    block_lst = markdown_to_blocks(markdown)
    html_blocks_lst = []
    for block in block_lst:
        block_type = block_to_block_type(block)
        html_blocks_lst.append(block_to_html_node(block, block_type))
    parent_node = ParentNode("div", html_blocks_lst)
    return parent_node


def block_to_html_node(text, block_type):
    if block_type == block_type_paragraph:
        return html_node_paragraph(text)
    if block_type == block_type_heading:
        return html_node_heading(text)
    if block_type == block_type_code:
        return html_node_code(text)
    if block_type == block_type_quote:
        return html_node_quote(text)
    if block_type == block_type_olist:
        return html_node_ordered_list(text)
    if block_type == block_type_ulist:
        return html_node_unordered_list(text)


def html_node_paragraph(text):
    lines = text.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def html_node_heading(text):
    i = 0
    for letter in text:
        if letter == "#":
            i += 1
        else:
            break
    if i + 1 >= len(text):
        raise ValueError(f"Invalid heading level: {i}")
    text = text.lstrip("#")
    text = text.strip()
    children = text_to_children(text)
    return ParentNode(f"h{i}", children)


def html_node_code(text):
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("Invalid code block")
    text = text.strip("```")
    children = text_to_children(text)
    return ParentNode("pre", [ParentNode("code", children)])


def html_node_quote(text: str):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith("> "):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def html_node_ordered_list(text):
    children = []
    lines = text.split("\n")
    i = 1
    for line in lines:
        line = line[3:]
        children.append(ParentNode("li", text_to_children(line)))
        i += 1
    return ParentNode("ol", children)


def html_node_unordered_list(text):
    children = []
    lines = text.split("\n")
    for line in lines:
        line = line[2:]
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


            
