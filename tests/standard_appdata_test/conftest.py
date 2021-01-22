import pytest
from gidappdata import AppDataStorager, ParaStorageKeeper
import os
import shutil
from gidappdata.utility.functions import readit, writeit, writebin, create_folder, writejson, pickleit, pathmaker
from .bin_data import bin_archive_data

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


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


@pytest.fixture(scope="session")
def construction_env():
    path = pathmaker(THIS_FILE_DIR, 'construction_info.env')
    author_name = "BrocaProgs"
    app_name = "Test_App"
    with open(path, 'w') as const_file:
        const_file.write("USES_BASE64=True\n")
        const_file.write(f"AUTHOR_NAME={author_name}\n")
        const_file.write(f"APP_NAME={app_name}")
    yield author_name, app_name
    os.remove(path)


@pytest.fixture(scope="session")
def deployed_supportkeeper(construction_env):
    save_path = pathmaker(os.getenv('APPDATA'), construction_env[0], construction_env[1])
    ParaStorageKeeper.set_archive_data(bin_archive_data)
    print(ParaStorageKeeper.get_appdata())
    yield ParaStorageKeeper.get_appdata(), save_path
    shutil.rmtree(os.path.dirname(save_path))
    assert os.path.isdir(os.path.dirname(save_path)) is False
