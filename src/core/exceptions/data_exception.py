

class DataException(Exception):
    def __init__(self, message, error_code, *args: object) -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(*args)