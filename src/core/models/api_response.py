from .error import Error

class ApiResponse:
    def __init__(self, result:any, error:Error):
        self.result: any = result
        self.error: Error = error
        self.is_successful: bool = self.error is None