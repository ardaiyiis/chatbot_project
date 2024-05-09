from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class CompanySetting(BaseEntity): 
    company_id = Column('CompanyId', Integer, ForeignKey('Company.Id'))
    company = relationship('Company')
    name_of_the_bot = Column('NameOfTheBot', String(200))
    general_prompt = Column('GeneralPrompt', String(500))
    welcome_message = Column('WelcomeMessage', String(500))
