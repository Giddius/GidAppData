import pytest
from gidappdata.cli.skeleton_tree import SkeletonInstructionItem, SkeletonTypus
from tempfile import TemporaryDirectory
from gidappdata.utility.functions import readbin, readit, pathmaker
import os

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def temp_root_dir():
    with TemporaryDirectory() as tempdir:
        yield tempdir


@pytest.fixture
def simple_directory_tree():
    item_dict = {
        'first_folder': [('first_subfolder', SkeletonTypus.Folder, None),
                         ('second_subfolder', SkeletonTypus.Folder, None),
                         ('first_folder_image_file.jpg', SkeletonTypus.File, readbin(pathmaker(THIS_FILE_DIR, 'afa_logoover_ca.jpg'))),
                         ('first_folder_ini_file.ini', SkeletonTypus.File, readit(pathmaker(THIS_FILE_DIR, 'example_cfg.ini')))]
    }
    root = SkeletonInstructionItem(name='root', typus=SkeletonTypus.Root)
    root.add_child_item(SkeletonInstructionItem(name='first_folder', typus=SkeletonTypus.Folder))
    root.add_child_item(SkeletonInstructionItem(name='second_folder', typus=SkeletonTypus.Folder))
    root.add_child_item(SkeletonInstructionItem(name='text_file.txt', typus=SkeletonTypus.File, content='this is a test text'))
    for key, value in item_dict.items():
        for _name, _typus, _content in value:
            root.children[key].add_child_item(SkeletonInstructionItem(name=_name, typus=_typus, content=_content))
    yield root
