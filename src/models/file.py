from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import BINARY
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class File(BaseEntity):
    name = Column('Name', String)
    content = Column('Content', BINARY)
    file_extension = Column('FileExtension', String)
    function_id = Column('FunctionId', Integer, ForeignKey('Function.Id'))
    function = relationship('Function')

