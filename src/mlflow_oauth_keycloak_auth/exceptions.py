
class MissingEnvironmentVariableException(Exception):
    """Exception raised when a required environment variable is missing
    """

    def __init__(self, variable_name):
        self.variable_name = variable_name
        self.message = f"Environment variable {variable_name} is missing"
        super().__init__(self.message)
