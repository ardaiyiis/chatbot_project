from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity
from datetime import datetime

class Message(BaseEntity):
    conversation_id = Column('ConversationId', Integer, ForeignKey('Conversation.Id'))
    role = Column('Role', String)
    content = Column('Content', String)
    conversation = relationship('Conversation')
    created_at = Column('CreatedAt', TIMESTAMP, server_default=func.now(), default=datetime.utcnow)
    created_by_id = Column('CreatedById', Integer, default=1)
    last_updated_by = Column('LastUpdatedById', Integer, default=1)