import os
import shutil
import click
from gidappdata.utility.functions import pathmaker, create_folder, create_file


def create_dev_env_trigger(in_path):
    _path = pathmaker(in_path, 'dev_env.trigger')
    create_file(_path, '')


def create_skeleton(in_path):
    pass
