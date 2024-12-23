import os
import shutil

from copystatic import copy_dir
from generatepage import generate_page


dir_path_static = "./static"
dir_path_public = "./public"
template_path = "./template.html"
dir_path_content = "./content"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_dir(dir_path_static, dir_path_public)
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html"),
    )


main()
