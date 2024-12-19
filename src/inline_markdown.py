from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_lst = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            lst_node = node.text.split(delimiter)
            if len(lst_node) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            split_nodes = []
            for i in range(len(lst_node)):
                if lst_node[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(lst_node[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(lst_node[i], text_type))
            result_lst.extend(split_nodes)
        else:
            result_lst.append(node)
    return result_lst


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_link(old_nodes):
    return _split_nodes_with_markdown(
        old_nodes, extract_markdown_links, TextType.LINK, "[{text}]({url})"
    )


def split_nodes_image(old_nodes):
    return _split_nodes_with_markdown(
        old_nodes, extract_markdown_images, TextType.IMAGE, "![{text}]({url})"
    )


def _split_nodes_with_markdown(
    old_nodes, extract_function, text_type, markdown_pattern
):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted = extract_function(node.text)
        if text_type == TextType.LINK:
            if (
                ("[" in node.text and "]" not in node.text)
                or ("]" in node.text and "(" not in node.text)
                or ("[" not in node.text and "](" in node.text)
                or ("(" in node.text and ")" not in node.text)
            ) and not extracted:
                raise ValueError("Invalid markdown, link section not closed")
        elif text_type == TextType.IMAGE:
            if (
                ("![" in node.text and "]" not in node.text)
                or ("]" in node.text and "(" not in node.text)
                or ("![" not in node.text and "](" in node.text)
                or ("(" in node.text and ")" not in node.text)
            ) and not extracted:
                raise ValueError("Invalid markdown, image section not closed")
        if not extracted:
            new_nodes.append(node)
            continue
        tuple = extracted[0]
        if tuple[0] == "" or tuple[1] == "":
            raise ValueError("Invalid markdown, text or url cannot be empty")
        pattern = markdown_pattern.format(text=tuple[0], url=tuple[1])
        sections = node.text.split(pattern, 1)
        if sections[0] != "":
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(f"{tuple[0]}", text_type, f"{tuple[1]}"))
        if len(sections) > 1:
            split_function = (
                split_nodes_image if text_type == TextType.IMAGE else split_nodes_link
            )
            new_nodes.extend(split_function([TextNode(sections[1], TextType.TEXT)]))

    return new_nodes


def text_to_textnodes(text):
    result_list = split_nodes_delimiter(
        split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_image(split_nodes_link([TextNode(text, TextType.TEXT)])),
                "**",
                TextType.BOLD,
            ),
            "*",
            TextType.ITALIC,
        ),
        "`",
        TextType.CODE,
    )
    return result_list
