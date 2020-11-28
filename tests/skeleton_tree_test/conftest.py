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
    print('closed temp dir')


@pytest.fixture
def simple_directory_tree():

    item_dict = {
        'first_folder': [('first_subfolder', SkeletonTypus.Folder, None),
                         ('second_subfolder', SkeletonTypus.Folder, None),
                         ('first_folder_image_file.jpg', SkeletonTypus.File, readbin(pathmaker('tests', 'skeleton_tree_test', 'afa_logoover_ca.jpg'))),
                         ('first_folder_ini_file.ini', SkeletonTypus.File, readit(pathmaker('tests', 'skeleton_tree_test', 'example_cfg.ini')))],
        'second_folder': [('something_file.txt', SkeletonTypus.File, 'this')]}
    root = SkeletonInstructionItem(name='root', typus=SkeletonTypus.Root)
    root.add_child_item(SkeletonInstructionItem(name='first_folder', typus=SkeletonTypus.Folder))
    root.add_child_item(SkeletonInstructionItem(name='second_folder', typus=SkeletonTypus.Folder))
    root.add_child_item(SkeletonInstructionItem(name='text_file.txt', typus=SkeletonTypus.File, content='this is a test text'))

    for key, value in item_dict.items():
        for _name, _typus, _content in value:
            getattr(root, key).add_child_item(SkeletonInstructionItem(name=_name, typus=_typus, content=_content))
    root.first_folder.first_subfolder.add_child_item(SkeletonInstructionItem(name='nested_test.json', typus=SkeletonTypus.File, content='{}'))
    yield root


@pytest.fixture
def access_test_tree():
    root = SkeletonInstructionItem(name='root', typus=SkeletonTypus.Root)
    first_folder_item = SkeletonInstructionItem(name='first_folder', typus=SkeletonTypus.Folder)
    second_folder_item = SkeletonInstructionItem(name='second_folder', typus=SkeletonTypus.Folder)
    first_sub_folder_item = SkeletonInstructionItem(name='first_sub_folder', typus=SkeletonTypus.Folder)
    sub_folder_file_item = SkeletonInstructionItem(name='sub_folder_file.txt', typus=SkeletonTypus.File, content='this is a subfolder txt file')
    root.add_child_item(first_folder_item)
    root.add_child_item(second_folder_item)
    first_folder_item.add_child_item(first_sub_folder_item)
    first_sub_folder_item.add_child_item(sub_folder_file_item)
    yield root, first_folder_item, second_folder_item, first_sub_folder_item, sub_folder_file_item
