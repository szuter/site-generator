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
    with open(dest_path,"w") as html_file:
        html_file.write(template)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_type_heading == block_to_block_type(block) and block.startswith("# "):
            return block.strip("# ").strip()
    raise Exception("Invalid heading")
