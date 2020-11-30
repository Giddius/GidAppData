import os
import shutil
import click
from dotenv import load_dotenv, find_dotenv
from gidappdata.utility.functions import pathmaker, create_folder, create_file, loadjson
from gidappdata.utility.extended_dotenv import find_dotenv_everywhere
from gidappdata.cli.skeleton_tree import serialize_all_prebuilts, DirSkeletonReader, SkeletonInstructionItem, get_all_prebuilts
from pprint import pprint
from gidappdata.cli.tree_render import print_tree

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


@click.command()
@click.argument('target_dir')
@click.argument('skeleton_selection')
@click.option('-c', '--skeleton-category', default=None)
@click.option('--overwrite/--no-overwrite', '-o/-no', default=False)
def build_target_skeleton(target_dir, skeleton_selection, skeleton_category, overwrite):
    path = pathmaker(target_dir, 'init_userdata')
    skeleton_tree = select_skeleton(skeleton_selection, skeleton_category)
    skeleton_tree.set_root_path(pathmaker(path, skeleton_tree.name))
    skeleton_tree.start_build(overwrite=overwrite)
    create_file(pathmaker(path, '__init__.py'), '')
    create_dev_env_trigger(path)
    create_user_data_setup(path)


@click.command()
@click.option('--tree/--no-tree', '-t/-nt', default=True)
def list_available(tree):
    all_prebuilts = get_all_prebuilts()

    for category, value in all_prebuilts.items():
        category = category.replace('prebuilt_', '')
        for name, path in value.items():

            print('\n\n#################################\n')
            print('Category: ' + category.upper() + ' --> ' + 'Name: ' + name)
            if tree:
                path = os.path.dirname(path)
                print_tree(path, category)
            print('\n#################################\n\n')


if __name__ == '__main__':
    list_available()
