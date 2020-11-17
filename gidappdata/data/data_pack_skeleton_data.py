from collections import namedtuple
skeleton_item = namedtuple('SkeletonItem', ['name', 'typus', 'content'], defaults=[''])


SUBPACKAGE_FOLDER = skeleton_item('init_appdata_storage', 'folder')
DATAPACK_FOLDER = skeleton_item('data_pack', 'folder')
CONFIG_FOLDER = skeleton_item('config', 'folder')
FIXED_DATA_FOLDER = skeleton_item('fixed_data', 'folder')
IMAGE_FILES_FOLDER = skeleton_item('image_files', 'folder')
MISC_FOLDER = skeleton_item('misc', 'folder')
PLUGINS_FOLDER = skeleton_item('plugins', 'folder')
USER_DATA_FOLDER = skeleton_item('user_data', 'folder')

SKELETON_STRUCTURE = {SUBPACKAGE_FOLDER: [{DATAPACK_FOLDER: [{CONFIG_FOLDER:[]}]}]}
