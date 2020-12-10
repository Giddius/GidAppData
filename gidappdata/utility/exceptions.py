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
