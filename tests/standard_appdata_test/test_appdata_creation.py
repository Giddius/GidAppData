from gidappdata import AppDataStorager
import pytest
import os
from gidappdata.utility.functions import readit, writeit, writebin, create_folder, writejson, pickleit, pathmaker, loadjson
import sys
import appdirs


def test_created_folder(simple_appdata_storage):
    assert simple_appdata_storage.appstorage_folder == pathmaker(appdirs.user_data_dir(appauthor='test_author', appname='test_app_name', roaming=True))
    assert simple_appdata_storage.log_folder == pathmaker(appdirs.user_log_dir(appauthor='test_author', appname='test_app_name', opinion=True))
    assert os.path.exists(simple_appdata_storage.appstorage_folder) is True
    assert os.path.exists(simple_appdata_storage.log_folder) is True
    assert os.listdir(simple_appdata_storage.log_folder) == []
    assert os.listdir(simple_appdata_storage.appstorage_folder) == []


@ pytest.mark.skipif(sys.platform != 'win32', reason="paths are specific to windows")
def test_folder_file_access(filled_appdata_storage):
    assert filled_appdata_storage['first_folder'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder"
    assert os.path.isdir(filled_appdata_storage['first_folder']) is True

    assert filled_appdata_storage['data_subfolder'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/data_subfolder"
    assert os.path.isdir(filled_appdata_storage['data_subfolder']) is True

    assert filled_appdata_storage['image_subfolder'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/image_subfolder"
    assert os.path.isdir(filled_appdata_storage['image_subfolder']) is True

    assert filled_appdata_storage['test_image.jpg'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/image_subfolder/test_image.jpg"
    assert os.path.isfile(filled_appdata_storage['test_image.jpg']) is True

    assert filled_appdata_storage['test_image.png'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/image_subfolder/test_image.png"
    assert os.path.isfile(filled_appdata_storage['test_image.png']) is True

    assert filled_appdata_storage['test_image.ico'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/image_subfolder/test_image.ico"
    assert os.path.isfile(filled_appdata_storage['test_image.ico']) is True

    assert filled_appdata_storage['test_1.txt'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/data_subfolder/test_1.txt"
    assert os.path.isfile(filled_appdata_storage['test_1.txt']) is True
    assert readit(filled_appdata_storage['test_1.txt']) == 'this is a test text file!'

    assert filled_appdata_storage['test_2.txt'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/data_subfolder/test_2.txt"
    assert os.path.isfile(filled_appdata_storage['test_2.txt']) is True
    assert readit(filled_appdata_storage['test_2.txt']) == 'this is another test text file!'

    assert filled_appdata_storage['test_dict.json'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/data_subfolder/test_dict.json"
    assert os.path.isfile(filled_appdata_storage['test_dict.json']) is True
    assert loadjson(filled_appdata_storage['test_dict.json']) == {}

    assert filled_appdata_storage['data_subfolder/some_file_not_real.txt'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/first_folder/data_subfolder/some_file_not_real.txt"
    assert os.path.isdir(filled_appdata_storage['data_subfolder/some_file_not_real.txt']) is False

    assert filled_appdata_storage['fake_folder'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/fake_folder"
    assert os.path.isdir(filled_appdata_storage['fake_folder']) is False

    assert filled_appdata_storage['fake_file.txt'] == "C:/Users/Giddi/AppData/Roaming/test_author/test_app_name/unfoldered_files/fake_file.txt"
    assert os.path.isdir(filled_appdata_storage['fake_file.txt']) is False


def test_clear(filled_appdata_storage):
    main_folder = str(filled_appdata_storage).rsplit('/', 2)[0]

    assert os.path.isdir(main_folder) is True
    assert os.path.isdir(str(filled_appdata_storage)) is True
    assert os.path.isdir(filled_appdata_storage.log_folder) is True

    filled_appdata_storage.clean(filled_appdata_storage.AllFolder)

    assert os.path.isdir(str(filled_appdata_storage)) is False
    assert os.path.isdir(filled_appdata_storage.log_folder) is False
    assert os.path.isdir(main_folder) is True
