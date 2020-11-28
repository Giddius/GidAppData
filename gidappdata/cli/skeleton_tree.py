# region [Imports]

# * Standard Library Imports -->
import gc
import os
import re
import sys
import json
import lzma
import time
import queue
import logging
import platform
import subprocess
from enum import Enum, Flag, auto
from time import sleep
from pprint import pprint, pformat
from typing import Union
from datetime import tzinfo, datetime, timezone, timedelta
from functools import wraps, lru_cache, singledispatch, total_ordering, partial
from contextlib import contextmanager
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# * Third Party Imports -->
# import requests
# import pyperclip
# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from github import Github, GithubException
# from jinja2 import BaseLoader, Environment
# from natsort import natsorted
# from fuzzywuzzy import fuzz, process

# * Gid Imports -->
import gidlogger as glog

from gidappdata.utility import readit, readbin, writebin, writeit, writejson, loadjson, linereadit, pathmaker, create_folder, create_file, clearit, pickleit, get_pickled, read_file
import base64

# endregion[Imports]

__updated__ = '2020-11-23 20:47:14'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]


def json_parts(item):
    if item.typus is not SkeletonTypus.Root:
        yield (item.parent.name, item.name, item.typus.value, item.content)

    if item.typus is not SkeletonTypus.File:
        for child in item.children:
            yield from json_parts(child)


def json_it(item, _file):
    _out = {}
    for _parent, _name, _typus, _content in json_parts(item):
        if _parent not in _out:
            _out[_parent] = []
        if isinstance(_content, bytes):
            _content = base64.b64encode(_content)
        _out[_parent].append((_name, _typus, _content))
    writejson(_out, _file, indent=2, sort_keys=False)


class SkeletonTypus(Enum):
    Folder = 'folder'
    File = 'file'
    Root = 'root'


class SkeletonInstructionBaseItem:
    pass


class SkeletonInstructionItem(SkeletonInstructionBaseItem):
    serialize_strategies = {'pickle': (pickleit, '.pkl'), 'json': (json_it, '.json')}

    def __init__(self, name: str, typus: SkeletonTypus, parent: SkeletonInstructionBaseItem = None, content=None):
        self.name = name
        self.typus = typus
        self.parent = parent
        self.children = [] if self.typus in [SkeletonTypus.Folder, SkeletonTypus.Root] else None
        self.content = content

    @staticmethod
    def _make_child_keyname(child):
        return child.name.replace('.', '__')

    def add_child_item(self, new_child: SkeletonInstructionBaseItem):
        if self.typus is SkeletonTypus.File:
            raise AttributeError("Files can not have children Items")
        if any(new_child.name.casefold() == existing_child.name.casefold() for existing_child in self.children):
            raise FileExistsError(f"The {new_child.typus.value} {new_child.name} already exist inside this Folder")
        self.children.append(new_child)
        new_child.parent = self

    @property
    def path(self):
        if self.parent is None or self.typus is SkeletonTypus.Root:
            return pathmaker(self.name)
        else:
            return pathmaker(self.parent.path, self.name)

    def set_root_path(self, root_path):
        if self.typus is SkeletonTypus.Root:
            self.name = root_path
        elif self.parent is None:
            raise AttributeError("This method can not be used on items that are not linked utimately to an ROOT Item")
        else:
            self.parent.set_root_path(root_path)

    def get_paths(self):
        yield self.path
        if self.typus is not SkeletonTypus.File:
            for child in self.children:
                yield from child.get_paths()

    def _build(self, overwrite=False):
        if self.typus is SkeletonTypus.Root:
            create_folder(self.path, False)
        elif self.typus is SkeletonTypus.Folder:
            create_folder(self.path, overwrite=overwrite)

        elif self.typus is SkeletonTypus.File:
            content = '' if self.content is None else self.content
            create_file(self.path, content, overwrite=overwrite)

        if self.children is not None:
            for child in self.children:
                child._build(overwrite=overwrite)

    def start_build(self, overwrite=False, from_top=True):
        if self.typus is not SkeletonTypus.Root and from_top is True:
            if self.parent is not None:
                self.parent.start_build(overwrite, from_top)
            else:
                raise AttributeError("This method with the argument 'from_top'=True can not be used on items that are not linked utimately to an ROOT Item")
        else:
            self._build(overwrite)

    def serialize(self, save_file_path, strategy='json', from_top=True):
        if self.typus is not SkeletonTypus.Root and from_top is True:
            if self.parent is not None:
                self.parent.serialize(save_file_path, strategy, from_top)
            else:
                raise AttributeError("This method with the argument 'from_top'=True can not be used on items that are not linked utimately to an ROOT Item")
        elif self.typus is not SkeletonTypus.Root and from_top is False:
            self.parent = None
            _func, _extension = self.serialize_strategies[strategy]
            _file = save_file_path + _extension if '.' not in os.path.basename(save_file_path) else save_file_path
            _func(self, _file)
        elif self.typus is SkeletonTypus.Root:
            _func, _extension = self.serialize_strategies[strategy]
            _file = save_file_path + _extension if '.' not in os.path.basename(save_file_path) else save_file_path
            _func(self, _file)

    def __getattr__(self, name):
        _out = None
        for child in self.children:
            if self._make_child_keyname(child).casefold() == name.casefold():
                _out = child
        if _out is None:
            raise AttributeError(name)
        return _out

    def all_nodes(self):
        if self.parent is not None:
            self.parent.all_nodes()
        else:
            yield self.name, self
            yield from self._all_nodes_walker()

    def _all_nodes_walker(self):
        if self.typus is not SkeletonTypus.File:
            for child_item in self.children:
                yield child_item.name, child_item
                yield from child_item._all_nodes_walker()

    def find_node(self, name):
        for node_name, node_object in self.all_nodes():
            if node_name.casefold() == name.casefold():
                return node_object


class DirSkeletonReader:
    exclude = {'__pycache__', '.git'}
    exclude = set(map(lambda x: x.casefold(), exclude))

    def __init__(self, start_folder_path):
        self.start_folder_path = start_folder_path
        self.start_folder_name = os.path.basename(self.start_folder_path)
        self.skeleton_tree = None
        self._make_skeleton_tree()

    def _make_skeleton_tree(self):
        self.skeleton_tree = SkeletonInstructionItem(self.start_folder_name, SkeletonTypus.Root)
        for dirname, folderlist, filelist in os.walk(self.start_folder_path, followlinks=False):
            if all(ex_item.casefold() not in dirname.casefold() for ex_item in self.exclude):
                parent = os.path.basename(dirname)
                for foldername in folderlist:
                    if foldername.casefold() not in self.exclude:
                        self.skeleton_tree.find_node(parent).add_child_item(SkeletonInstructionItem(foldername, SkeletonTypus.Folder))
                for filename in filelist:
                    if filename.casefold() not in self.exclude:
                        self.skeleton_tree.find_node(parent).add_child_item(SkeletonInstructionItem(filename, SkeletonTypus.File, content=read_file(pathmaker(dirname, filename))))

    def rename_node(self, node_name, new_name):
        node = self.find_node(node_name)
        node.name = new_name

    def __getattr__(self, name):
        return getattr(self.skeleton_tree, name)


def quick_check_skeleton():
    item_dict = {
        'first_folder': [('first_subfolder', SkeletonTypus.Folder, None),
                         ('second_subfolder', SkeletonTypus.Folder, None),
                         ('first_folder_image_file.jpg', SkeletonTypus.File, readbin(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidAppData\tests\skeleton_tree_test\afa_logoover_ca.jpg")),
                         ('first_folder_ini_file.ini', SkeletonTypus.File, readit(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidAppData\tests\skeleton_tree_test\example_cfg.ini"))],
        'second_folder': [('something_file.txt', SkeletonTypus.File, 'this')]}
    root = SkeletonInstructionItem(name='root', typus=SkeletonTypus.Root)
    root.add_child_item(SkeletonInstructionItem(name='first_folder', typus=SkeletonTypus.Folder))
    root.add_child_item(SkeletonInstructionItem(name='second_folder', typus=SkeletonTypus.Folder))
    root.add_child_item(SkeletonInstructionItem(name='text_file.txt', typus=SkeletonTypus.File, content='this is a test text'))

    for key, value in item_dict.items():
        for _name, _typus, _content in value:
            root.children[key].add_child_item(SkeletonInstructionItem(name=_name, typus=_typus, content=_content))
    root.first_folder.first_subfolder.add_child_item(SkeletonInstructionItem(name='nested_test.json', typus=SkeletonTypus.File, content='{}'))
    print(root.find_node('first_folder_ini_file.ini').name)


# region[Main_Exec]

if __name__ == '__main__':
    x = DirSkeletonReader(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\PyQt_Socius\pyqtsocius\init_userdata\data_pack")

    x.serialize('test_serial')
# endregion[Main_Exec]
