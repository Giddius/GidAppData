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

from gidappdata.utility import readit, readbin, writebin, writeit, writejson, loadjson, linereadit, pathmaker, create_folder, create_file, clearit, pickleit, get_pickled


# endregion[Imports]

__updated__ = '2020-11-17 13:20:10'

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]


class SkeletonTypus(Enum):
    Folder = 'folder'
    File = 'file'
    Root = 'root'


class SkeletonInstructionBaseItem:
    pass


class SkeletonInstructionItem(SkeletonInstructionBaseItem):
    serialize_strategies = {'pickle': (pickleit, '.pkl')}

    def __init__(self, name: str, typus: SkeletonTypus, parent: SkeletonInstructionBaseItem = None, content=None):
        self.name = name
        self.typus = typus
        self.parent = parent
        self.children = {} if self.typus in [SkeletonTypus.Folder, SkeletonTypus.Root] else None
        self.content = content

    def add_child_item(self, new_child: SkeletonInstructionBaseItem):
        if self.typus is SkeletonTypus.File:
            raise AttributeError("Files can not have children Items")

        if any(new_child.name.casefold() == existing_child_name.casefold() for existing_child_name in self.children):
            raise FileExistsError(f"The {new_child.typus.value} already exist inside this Folder")
        self.children[new_child.name] = new_child
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
            for _name, child in self.children.items():
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
            for _name, child in self.children.items():
                child._build(overwrite=overwrite)

    def start_build(self, overwrite=False, from_top=True):
        if self.typus is not SkeletonTypus.Root and from_top is True:
            if self.parent is not None:
                self.parent.start_build(overwrite, from_top)
            else:
                raise AttributeError("This method with the argument 'from_top'=True can not be used on items that are not linked utimately to an ROOT Item")
        else:
            self._build(overwrite)

    def serialize(self, save_file_path, strategy='pickle', from_top=True):
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

        # region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
