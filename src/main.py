import os
import shutil

from copystatic import copy_dir
from generatepage import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./public"
template_path = "./template.html"
dir_path_content = "./content"


def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_dir(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


main()
