from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity
class FunctionKey(BaseEntity): 
    function_id = Column('FunctionId', Integer, ForeignKey('Function.Id'))
    key_id = Column('KeyId', Integer, ForeignKey('Key.Id'))
    key = relationship('Key')
    is_required = Column('IsRequired', Boolean)
