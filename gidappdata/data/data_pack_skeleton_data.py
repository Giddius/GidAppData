import os
from gidappdata.cli.skeleton_tree import DirSkeletonReader
from gidappdata.utility.functions import pathmaker


THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
STANDARD = pathmaker(THIS_FILE_DIR, 'prebuilt_standard')
SERIALIZE_SKELETONS_FOLDER = pathmaker(THIS_FILE_DIR, 'serialized_skeletons')


def selection_dict():
    _out = {}
    for item in os.scandir(THIS_FILE_DIR):
        if os.path.isdir(item.path) and item.name.startswith('prebuilt_'):
            _name = item.name.replace('prebuilt_', '')
            _out[_name] = pathmaker(item.path)
    return _out


def make_tree(selection_name=None):
    _source_path = selection_dict().get(selection_name, STANDARD)
    root = DirSkeletonReader(_source_path)
    print(list(root.get_paths()))
    root.serialize(pathmaker(SERIALIZE_SKELETONS_FOLDER, os.path.basename(_source_path)))


if __name__ == '__main__':
    root = DirSkeletonReader(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\GidAppData\tools")
    root.serialize(pathmaker(SERIALIZE_SKELETONS_FOLDER, 'testing'))
    for ix, xi in root.all_nodes():
        print(ix)
