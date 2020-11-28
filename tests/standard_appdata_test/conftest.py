import pytest
from gidappdata import AppDataStorager
import os
import shutil
from gidappdata.utility.functions import readit, writeit, writebin, create_folder, writejson, pickleit, pathmaker


@pytest.fixture
def simple_appdata_storage():
    appdata = AppDataStorager('test_author', 'test_app_name')
    yield appdata
    try:
        appdata.clean(appdata.AllFolder)
    except FileNotFoundError as error:
        print(str(error))


@pytest.fixture
def filled_appdata_storage(simple_appdata_storage):
    _first_folder = pathmaker(str(simple_appdata_storage), 'first_folder')
    create_folder(_first_folder)
    create_folder(pathmaker(_first_folder, 'data_subfolder'))
    create_folder(pathmaker(_first_folder, 'image_subfolder'))
    writeit(pathmaker(_first_folder, 'data_subfolder', 'test_1.txt'), 'this is a test text file!')
    writeit(pathmaker(_first_folder, 'data_subfolder', 'test_2.txt'), 'this is another test text file!')
    writejson({}, pathmaker(_first_folder, 'data_subfolder', 'test_dict.json'))
    source_folder = pathmaker('tests', 'standard_appdata_test')
    target_folder = pathmaker(_first_folder, 'image_subfolder')
    images = ['test_image.ico', 'test_image.jpg', 'test_image.png']
    for image in images:
        shutil.copyfile(pathmaker(source_folder, image), pathmaker(target_folder, image))
    yield simple_appdata_storage
