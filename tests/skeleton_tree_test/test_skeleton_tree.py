import pytest
from gidappdata.cli.skeleton_tree import SkeletonInstructionItem, SkeletonTypus, DirSkeletonReader
from gidappdata.utility.functions import readbin, readit, pathmaker, loadjson
import os

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

RESTRUCTURE_REASON = "implementing new child Item method soon"


def helper_child_walker(tree, name):
    for child in tree.children:
        if child.name == name:
            return child


def test_child_access(access_test_tree):
    root, first_folder_item, second_folder_item, first_sub_folder_item, sub_folder_file_item = access_test_tree
    assert root.first_folder is first_folder_item
    assert root.first_folder.first_sub_folder is first_sub_folder_item
    assert root.second_folder is second_folder_item
    with pytest.raises(AttributeError):
        assert root.non_existing_file__ini
    assert root.first_folder.first_sub_folder.sub_folder_file__txt is sub_folder_file_item


def test_paths(simple_directory_tree, temp_root_dir):
    assert set(simple_directory_tree.get_paths()) == set(['root',
                                                          'root/first_folder',
                                                          'root/first_folder/first_folder_image_file.jpg',
                                                          'root/first_folder/first_folder_ini_file.ini',
                                                          'root/first_folder/first_subfolder',
                                                          'root/first_folder/second_subfolder',
                                                          'root/second_folder',
                                                          'root/text_file.txt',
                                                          'root/first_folder/first_subfolder/nested_test.json',
                                                          'root/second_folder/something_file.txt'])
    simple_directory_tree.set_root_path(temp_root_dir)
    assert set(simple_directory_tree.get_paths()) == set([pathmaker(temp_root_dir),
                                                          pathmaker(temp_root_dir, 'first_folder'),
                                                          pathmaker(temp_root_dir, 'first_folder/first_folder_image_file.jpg'),
                                                          pathmaker(temp_root_dir, 'first_folder/first_folder_ini_file.ini'),
                                                          pathmaker(temp_root_dir, 'first_folder/first_subfolder'),
                                                          pathmaker(temp_root_dir, 'first_folder/second_subfolder'),
                                                          pathmaker(temp_root_dir, 'second_folder'),
                                                          pathmaker(temp_root_dir, 'text_file.txt'),
                                                          pathmaker(temp_root_dir, 'first_folder/first_subfolder/nested_test.json'),
                                                          pathmaker(temp_root_dir, 'second_folder', 'something_file.txt')])


def test_file_children(simple_directory_tree):
    with pytest.raises(AttributeError):
        simple_directory_tree.text_file__txt.add_child_item(SkeletonInstructionItem('this_raises_Error', SkeletonTypus.Folder))
    with pytest.raises(AttributeError):
        simple_directory_tree.text_file__txt.add_child_item(SkeletonInstructionItem('this_raises_Error.csv', SkeletonTypus.File, content='this,should,raise,an,AttributeError'))


def test_existing_children(simple_directory_tree):
    with pytest.raises(FileExistsError):
        simple_directory_tree.add_child_item(SkeletonInstructionItem('text_file.txt', SkeletonTypus.File, content='this should raise an FileExistsError'))


def test_root_instantiation():
    root = SkeletonInstructionItem('root', SkeletonTypus.Root)
    assert root.name == 'root'
    assert root.typus is SkeletonTypus.Root
    assert root.content is None
    assert root.parent is None
    assert root.children == []


def test_dynamic_path_attribute(temp_root_dir):
    root = SkeletonInstructionItem('root', SkeletonTypus.Root)
    folder_level_0 = SkeletonInstructionItem('0_level_folder', SkeletonTypus.Folder)
    folder_level_1 = SkeletonInstructionItem('1_level_folder', SkeletonTypus.Folder)
    file_level_1_1 = SkeletonInstructionItem('1_1_level_file', SkeletonTypus.File, content='Bla Bla Bla')
    root.add_child_item(folder_level_0)
    folder_level_0.add_child_item(folder_level_1)
    folder_level_0.add_child_item(file_level_1_1)
    assert root.path == pathmaker('root')
    assert folder_level_0.path == pathmaker('root', '0_level_folder')
    assert folder_level_1.path == pathmaker('root', '0_level_folder', '1_level_folder')
    assert file_level_1_1.path == pathmaker('root', '0_level_folder', '1_1_level_file')
    root.set_root_path(temp_root_dir)
    assert root.path == pathmaker(temp_root_dir)
    assert folder_level_0.path == pathmaker(temp_root_dir, '0_level_folder')
    assert folder_level_1.path == pathmaker(temp_root_dir, '0_level_folder', '1_level_folder')
    assert file_level_1_1.path == pathmaker(temp_root_dir, '0_level_folder', '1_1_level_file')


def test_set_root_path(simple_directory_tree, temp_root_dir):
    simple_directory_tree.set_root_path(temp_root_dir)
    assert simple_directory_tree.name == temp_root_dir
    assert simple_directory_tree.typus is SkeletonTypus.Root
    assert simple_directory_tree.path == pathmaker(temp_root_dir)
    first_folder = simple_directory_tree.first_folder
    assert first_folder.name == 'first_folder'
    assert first_folder.typus is SkeletonTypus.Folder
    assert first_folder.path == pathmaker(temp_root_dir, 'first_folder')
    subfolder = first_folder.first_subfolder
    assert subfolder.name == 'first_subfolder'
    assert subfolder.typus is SkeletonTypus.Folder
    assert subfolder.path == pathmaker(temp_root_dir, 'first_folder', 'first_subfolder')


def test_file_handling(simple_directory_tree):
    first_file = simple_directory_tree.text_file__txt
    assert first_file.children is None
    assert first_file.typus is SkeletonTypus.File


def test_build_correct_names(simple_directory_tree, temp_root_dir):
    simple_directory_tree.set_root_path(temp_root_dir)
    simple_directory_tree.start_build()
    assert set(os.listdir(temp_root_dir)) == set(['text_file.txt', 'second_folder', 'first_folder'])
    assert set(os.listdir(pathmaker(temp_root_dir, 'first_folder'))) == set(['first_subfolder', 'second_subfolder', 'first_folder_image_file.jpg', 'first_folder_ini_file.ini'])


def test_correct_file_content(simple_directory_tree, temp_root_dir):
    simple_directory_tree.set_root_path(temp_root_dir)
    simple_directory_tree.start_build()
    with open(pathmaker(temp_root_dir, 'text_file.txt'), 'r') as fp:
        assert fp.read() == 'this is a test text'
    with open(pathmaker(temp_root_dir, 'first_folder', 'first_folder_ini_file.ini'), 'r') as fpini:
        assert fpini.read() == readit(pathmaker('tests', 'skeleton_tree_test', 'example_cfg.ini'))
    with open(pathmaker(temp_root_dir, 'first_folder', 'first_folder_image_file.jpg'), 'rb') as fpb:
        assert fpb.read() == readbin(pathmaker('tests', 'skeleton_tree_test', "afa_logoover_ca.jpg"))


def test_find_node(simple_directory_tree):
    x = simple_directory_tree.find_node('second_subfolder')
    assert x.name == 'second_subfolder'
    assert x.typus == SkeletonTypus.Folder
    assert x.content is None
    y = simple_directory_tree.find_node('nested_test.json')
    assert y.name == 'nested_test.json'
    assert y.typus == SkeletonTypus.File
    assert y.content == '{}'


def test_serialize(tmpdir):
    source_dir = pathmaker(THIS_FILE_DIR, 'example_dir', 'data_pack')
    target = tmpdir.join('serialize_test.json')
    tree = DirSkeletonReader(source_dir)
    tree.serialize(target, strategy='json')
    assert loadjson(target) == loadjson(pathmaker(THIS_FILE_DIR, 'serialize_test_compare.json'))


def test_build_from_json(tmpdir):
    target = tmpdir.mkdir('test_tree_build')
    tree = SkeletonInstructionItem.from_json_file(pathmaker(THIS_FILE_DIR, 'serialize_test_compare.json'))
    tree.set_root_path(target)
    tree.start_build()
    for path in tree.get_paths():
        assert os.path.exists(path) is True
