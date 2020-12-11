import os
import shutil
import click
from dotenv import load_dotenv, find_dotenv
from gidappdata.utility.functions import pathmaker, create_folder, create_file, loadjson, appendwriteit
from gidappdata.utility.extended_dotenv import find_dotenv_everywhere
from gidappdata.cli.skeleton_tree import serialize_all_prebuilts, DirSkeletonReader, SkeletonInstructionItem, get_all_prebuilts
from pprint import pprint
from gidappdata.cli.tree_render import print_tree
from functools import partial
from textwrap import dedent


THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

SERIALIZED_DIR = pathmaker(DirSkeletonReader.serialized_prebuilts_folder)


def spec_appendwriteit(filepath, data):
    with open(filepath, 'a') as f:
        f.write(data + '\n')


def get_all_serialized_skeletons():
    serialize_all_prebuilts()
    _out = {}
    for serialized_skeleton in os.scandir(SERIALIZED_DIR):
        if os.path.isfile(serialized_skeleton) and serialized_skeleton.name.endswith('.json'):
            _out[serialized_skeleton.name.replace('.json', '')] = loadjson(serialized_skeleton.path)
    return _out


def create_user_data_setup(path):
    user_data_setup_file = pathmaker(path, 'user_data_setup.py')
    with open(user_data_setup_file, 'w') as uds_file:
        uds_file.write(dedent("""from gidappdata import SupportKeeper
                            from gidappdata.utility.extended_dotenv import find_dotenv_everywhere
                            import os
                            import dotenv
                            from .bin_data import bin_archive_data
                            dotenv.load_dotenv(find_dotenv_everywhere('project_meta_data.env'))

                            THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
                            DATA_DIR = os.path.join(THIS_FILE_DIR, 'data_pack')
                            CONSTRUCTION_INFO_FILE = os.path.join(THIS_FILE_DIR, 'construction_info.env')


                            if os.path.isfile(CONSTRUCTION_INFO_FILE):
                                dotenv.load_dotenv(CONSTRUCTION_INFO_FILE)

                            if os.path.isfile('dev.trigger') is True:
                                SupportKeeper.set_dev(True, DATA_DIR)
                            SupportKeeper.set_archive_data(bin_archive_data)
                            """))


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


def build_target_skeleton(target_dir, skeleton_selection, skeleton_category, overwrite):
    path = pathmaker(target_dir, 'init_userdata')
    skeleton_tree = select_skeleton(skeleton_selection, skeleton_category)
    skeleton_tree.set_root_path(pathmaker(path, skeleton_tree.name))
    skeleton_tree.start_build(overwrite=overwrite)
    create_file(pathmaker(path, '__init__.py'), '')
    create_dev_env_trigger(path)
    create_user_data_setup(path)


@click.group()
def cli():
    pass


@cli.command(name='build')
@click.argument('target_dir')
@click.argument('skeleton_selection')
@click.option('-c', '--skeleton-category', default=None)
@click.option('--overwrite/--no-overwrite', '-o/-no', default=False)
def to_build_target_skeleton(target_dir, skeleton_selection, skeleton_category, overwrite):
    build_target_skeleton(target_dir, skeleton_selection, skeleton_category, overwrite)


@cli.command(name='list')
@click.option('--tree/--no-tree', '-t/-nt', default=True)
@click.option('-t', '--to-file', default=None)
def list_available(tree, to_file):
    all_prebuilts = get_all_prebuilts()
    output_func = print if to_file is None else partial(spec_appendwriteit, to_file)
    for category, value in all_prebuilts.items():
        category = category.replace('prebuilt_', '')
        for name, path in value.items():

            output_func('\n\n#################################\n')
            output_func('Category: ' + category.upper() + ' --> ' + 'Name: ' + name)
            if tree:
                path = os.path.dirname(path)
                print_tree(path, category, output_function=output_func)
            output_func('\n#################################\n\n')


if __name__ == '__main__':
    cli()
