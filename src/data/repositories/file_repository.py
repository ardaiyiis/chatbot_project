from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from .base_repository import BaseRepository
from models import File, Function
from core.logging import SolomindLogger 


class FileRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger:SolomindLogger):
        super().__init__(session_factory, logger)

    def get_file_content(self, file_id:int):
        with self.session_factory() as session:
            return session.query(File).join(File.function).filter(File.Id == file_id).first()
        
    def get_file_content_by_function_name(self, function_name:str):
        with self.session_factory() as session:
            return session.query(File).join(File.function).filter(Function.name == function_name ).first()
        