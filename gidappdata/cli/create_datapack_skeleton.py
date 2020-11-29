import os
import shutil
import click
from dotenv import load_dotenv, find_dotenv
from gidappdata.utility.functions import pathmaker, create_folder, create_file, loadjson
from gidappdata.utility.extended_dotenv import find_dotenv_everywhere
from gidappdata.cli.skeleton_tree import serialize_all_prebuilts, DirSkeletonReader, SkeletonInstructionItem
from pprint import pprint

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

SERIALIZED_DIR = pathmaker(DirSkeletonReader.serialized_prebuilts_folder)


def get_all_serialized_skeletons():
    serialize_all_prebuilts()
    _out = {}
    for serialized_skeleton in os.scandir(SERIALIZED_DIR):
        if os.path.isfile(serialized_skeleton) and serialized_skeleton.name.endswith('.json'):
            _out[serialized_skeleton.name.replace('.json', '')] = loadjson(serialized_skeleton.path)
    return _out


def create_user_data_setup(path):
    pass


def create_dev_env_trigger(in_path):
    _path = pathmaker(in_path, 'dev.trigger')
    create_file(_path, '')


def select_skeleton(skeleton_selection, skeleton_category=None):
    category = 'standard' if skeleton_category is None else skeleton_category.casefold()
    selection = skeleton_selection.casefold()
    json_data = None
    all_serialized_skeletons = get_all_serialized_skeletons()
    for serialized_name in all_serialized_skeletons:
        if serialized_name.casefold() == f"[{category}]_{selection}":
            json_data = all_serialized_skeletons[serialized_name]
    if json_data is None:
        raise KeyError(f"unable to find serialized data for selection '{skeleton_selection}' and category '{category}'")
    return SkeletonInstructionItem.from_dict(json_data)


def build_target_skeleton(path, skeleton_selection, skeleton_category=None, overwrite=False):
    path = pathmaker(path, 'init_userdata')
    skeleton_tree = select_skeleton(skeleton_selection, skeleton_category)
    skeleton_tree.set_root_path(pathmaker(path, skeleton_tree.name))
    skeleton_tree.start_build(overwrite=overwrite)
    create_file(pathmaker(path, '__init__.py'), '')
    create_dev_env_trigger(path)
    create_user_data_setup(path)


if __name__ == '__main__':
    # build_target_skeleton(r"C:\Users\Giddi\Downloads\newfolder", 'basic')
    pass
