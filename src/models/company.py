from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import List 
from models.function import Function
from models.requirement import Requirement
from models.base_entity import BaseEntity
class Company(BaseEntity): 
 
    name = Column('Name',String(500))
    code = Column('Code',String(180))
    type_id = Column('TypeId',Integer, ForeignKey('CompanyType.Id'))
    type = relationship('CompanyType')
    logo = Column('Logo',String)
    assistant_id = Column('AssistantId')
    functions:Mapped[List["Function"]] = relationship('Function', back_populates='company')
    requirements:Mapped[List["Requirement"]] = relationship('Requirement', back_populates='company')
