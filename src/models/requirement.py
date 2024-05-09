from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from .base_entity import BaseEntity
from .requirement_key import RequirementKey
from typing import List

class Requirement(BaseEntity):
    company_id = Column('CompanyId', Integer, ForeignKey('Company.Id'))
    name = Column('Name', String(200))
    code = Column('Code', String(100))
    description = Column('Description', String(500))
    is_active = Column('IsActive', Boolean)
    question_to_user = Column('QuestionToUser', String(500)) 
    company = relationship('Company')
    keys:Mapped[List["RequirementKey"]] = relationship('RequirementKey', overlaps="requirement")
