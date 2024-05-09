from sqlalchemy import Column, String
from models.base_entity import BaseEntity

class DataLibraryType(BaseEntity):
    name = Column('Name', String(200))
    code = Column('Code', String(50))