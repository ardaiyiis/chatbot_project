from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped,deferred
from typing import List
from models.base_entity import BaseEntity
from models.function_key import FunctionKey

class Function(BaseEntity):
    company_id = Column('CompanyId', Integer, ForeignKey('Company.Id'))
    name = Column('Name', String(200))
    code = Column('Code', String(100))
    description = Column('Description', String(500))
    is_active = Column('IsActive', Boolean)
    data_library_type_id = Column('DataLibraryTypeId', Integer, ForeignKey('DataLibraryType.Id'))

    company = relationship('Company', back_populates='functions', uselist=False)  # Use 'company' as the relationship name
    data_library_type = relationship('DataLibraryType', uselist = False)
    data_library = relationship('File', back_populates='function', uselist=False)
    keys:Mapped[List["FunctionKey"]] = relationship('FunctionKey')