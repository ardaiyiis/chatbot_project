from sqlalchemy import Column, Integer, ForeignKey, String, func, TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity
class ChatUser(BaseEntity): 
    user_session_key = Column('UserSessionKey', String)
    company_id = Column('CompanyId', Integer, ForeignKey('Company.Id'))
    company = relationship('Company')
    conversation = relationship('Conversation')
    created_at = Column('CreatedAt', TIMESTAMP, server_default=func.now(), default=datetime.utcnow)
    created_by_id = Column('CreatedById', Integer, default=1)#For now
    last_updated_by = Column('LastUpdatedById', Integer, default=1)