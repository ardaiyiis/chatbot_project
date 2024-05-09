from sqlalchemy.ext.declarative import as_declarative,declared_attr
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
# Base = declarative_base()

@as_declarative()
class BaseEntity(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__
    id = Column('Id', Integer, primary_key=True)
    is_deleted = Column('IsDeleted', Boolean)
