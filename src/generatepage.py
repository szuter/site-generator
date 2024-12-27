from markdown_blocks import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_type_heading,
    block_to_block_type,
)
import os


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as from_file:
        markdown = from_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as html_file:
        html_file.write(template)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_type_heading == block_to_block_type(block) and block.startswith("# "):
            return block.strip("# ").strip()
    raise Exception("Invalid heading")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for item in os.listdir(dir_path_content):
        new_content_path = os.path.join(dir_path_content, item)
        new_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(new_content_path):
            new_dest_path = new_dest_path.replace(".md", ".html")
            generate_page(new_content_path, template_path, new_dest_path)
        elif os.path.isdir(new_content_path):
            generate_pages_recursive(new_content_path, template_path, new_dest_path)
