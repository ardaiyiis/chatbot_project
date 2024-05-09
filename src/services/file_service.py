from data.repositories import FileRepository

class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    def get_file_content(self, file_id):
        return self.file_repository.get_file_content(file_id)
    
    def get_file_content_by_function_name(self, function_name):
        return self.file_repository.get_file_content_by_function_name(function_name)
        
