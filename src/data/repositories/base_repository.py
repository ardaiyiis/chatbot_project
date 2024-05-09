 
from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from core.logging import SolomindLogger
class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger:SolomindLogger):
        self.session_factory =  session_factory
        self.logger = logger.get_logger(__name__)