import pytest
from gidappdata.cli.skeleton_tree import SkeletonInstructionItem, SkeletonTypus
from gidappdata.utility.functions import readbin, readit, pathmaker
import os


def test_build_simple_tree(simple_directory_tree, temp_root_dir):
    simple_directory_tree.set_root_path(temp_root_dir)
    simple_directory_tree.start_build()
    assert set(os.listdir(temp_root_dir)) == set(['text_file.txt', 'second_folder', 'first_folder'])
    assert set(os.listdir(pathmaker(temp_root_dir, 'first_folder'))) == set(['first_subfolder', 'second_subfolder', 'first_folder_image_file.jpg', 'first_folder_ini_file.ini'])
