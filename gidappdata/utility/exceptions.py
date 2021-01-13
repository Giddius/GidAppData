class GidAppDataBaseException(Exception):
    pass


class ConstructionEnvDataMissing(GidAppDataBaseException):
    def __init__(self, env_var_name):
        self.message = f"Variable '{env_var_name}' has not been set in the construction env file"
        super().__init__(self.message)


class DevSettingError(GidAppDataBaseException):
    def __init__(self):
        self.message = "'redirect' has to be an directory if 'dev' is set to 'True'"
        super().__init__(self.message)


class IsDuplicateNameError(GidAppDataBaseException):
    def __init__(self, name: str, full_path, is_file: bool = True):
        self.name = name
        self.full_path = full_path
        self.typus = "file" if is_file is True else "folder"
        self.msg = f"The {self.typus} name {self.name} ('{self.full_path}') already exists in this user_data dir, all file names and folder names need to be unique."
        super().__init__(self.msg)
