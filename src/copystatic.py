import os
import shutil


def copy_dir(scr_path, dst_path):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    for item in os.listdir(scr_path):
        item_path = os.path.join(scr_path, item)
        new_dst_path = os.path.join(dst_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, new_dst_path)
        elif os.path.isdir(item_path):
            copy_dir(item_path, new_dst_path)
