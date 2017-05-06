"""
Operative System utilities
"""
import os
import shutil

def copytree(src, dst, symlinks=False, ignore=None):
    """
    Copy a directory tree without creating de destination directory
    Idea from http://stackoverflow.com/questions/1868714
    """
    for item in os.listdir(src):
        src_file = os.path.join(src, item)
        dst_file = os.path.join(dst, item)
        if os.path.isdir(src_file):
            shutil.copytree(src_file, dst_file, symlinks, ignore)
        else:
            shutil.copy2(src_file, dst_file)
            