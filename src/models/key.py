from sqlalchemy import Column, Integer, String, ForeignKey
from models.base_entity import BaseEntity

class Key(BaseEntity):
    company_id = Column('CompanyId', Integer, ForeignKey('Company.Id'))
    name = Column('Name', String(200))
    code = Column('Code', String(100))
    description = Column('Description', String(500))
    type = Column('Type', String(200))
