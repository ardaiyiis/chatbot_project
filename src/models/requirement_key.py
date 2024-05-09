from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity

class RequirementKey(BaseEntity):
    requirement_id = Column('RequirementId', Integer, ForeignKey('Requirement.Id'))
    key_id = Column('KeyId', Integer, ForeignKey('Key.Id'))
    requirement = relationship('Requirement')
    key = relationship('Key')
