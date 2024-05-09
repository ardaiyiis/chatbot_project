from sqlalchemy import Column, Integer, ForeignKey, func, TIMESTAMP, String
from sqlalchemy.orm import relationship, Mapped
from typing import List
from datetime import datetime
from .base_entity import BaseEntity
from .message import Message
class Conversation(BaseEntity): 
    chat_user_id = Column('ChatUserId', Integer, ForeignKey('ChatUser.Id'))
    chat_user = relationship('ChatUser', overlaps='conversation')
    messages:Mapped[List["Message"]] = relationship('Message', back_populates='conversation')
    created_at = Column('CreatedAt', TIMESTAMP, server_default=func.now(), default=datetime.utcnow)
    created_by_id = Column('CreatedById', Integer, default=1)#For now
    last_updated_by = Column('LastUpdatedById', Integer, default=1)
    thread_id = Column('ThreadId', String)