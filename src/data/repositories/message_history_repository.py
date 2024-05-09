from .base_repository import BaseRepository
from models import Message, ChatUser, Conversation
from core.logging import SolomindLogger
from sqlalchemy.orm import Session, noload
from contextlib import AbstractContextManager
from typing import Callable
from core.exceptions import DataException
from datetime import datetime, timedelta


class MessageHistoryRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], logger: SolomindLogger):
        super().__init__(session_factory, logger)

    async def get_messages(self, user:ChatUser)-> list:
        with self.session_factory() as session:
            return session.query(Message)\
                        .join(Conversation)\
                        .filter(Conversation.chat_user == user)\
                        .order_by(Message.created_at.asc()).all()

    async def get_message_history(self, user_session_key, company_id:int) -> list:
        with self.session_factory() as session:
            user = await self.get_or_create_user(user_session_key, company_id=company_id)
            if user is not None:
                messages = await self.get_messages(user=user)
                current_time = datetime.now()
                # Check if the last message was created more than 30 minutes ago
                if messages and (current_time - messages[-2].created_at > timedelta(minutes=210)):
                    await self.delete_message_history(user_session_key, company_id=company_id, keep_last_message=True)
                    messages = await self.get_messages(user=user)

                if messages:
                    return [{"role": message.role, "content": message.content} for message in messages]
                else:
                    raise DataException(f"Message history with UserSessionKey '{user_session_key}' could not be found.", error_code="12007")
            else:
                raise DataException(f"User with UserSessionKey '{user_session_key}' could not be found.", error_code="12008")       

    async def insert_message(self, user_session_key, role:str, content:str, company_id:int, client=None):
        with self.session_factory() as session:
            # Insert a message into the database
            conversation = await self.get_latest_conversation(user_session_key, company_id, client)
            message = Message(conversation_id=conversation.id
                              , role=role, content=content
                              , is_deleted=False)
            session.add(message)
            session.commit()
        return "Message successfully inserted"


    async def delete_message_history(self, user_session_key, company_id:int, keep_last_message=False):
        with self.session_factory() as session:
            # Soft delete all messages in the conversation except the first one
            conversation = await self.get_latest_conversation(user_session_key, company_id)
            messages = session.query(Message).filter(
                            Message.conversation_id == conversation.id
                                ).order_by(Message.created_at).all()
            for i, message in enumerate(messages):
                if i == 0 or (keep_last_message and i == len(messages)- 1):
                    continue  # Skip the first message
                message.is_deleted = True
            session.commit()
        return "Message History successfully deleted"


    async def get_latest_conversation(self, user_session_key, company_id:int, client=None)->Conversation:
        # Implement the method to get the latest conversation for the user
        with self.session_factory() as session:
            conversation = session.query(Conversation)\
                                .join(Conversation.chat_user)\
                                    .filter(ChatUser.user_session_key == user_session_key, ChatUser.company_id == company_id).first()
            if conversation is None:
                # Create a new conversation if none exists
                thread = client.beta.threads.create()               
                user = await self.get_or_create_user(user_session_key, company_id) 
                conversation = Conversation(chat_user=user
                                            , is_deleted=False
                                            , thread_id = thread.id)
                session.add(conversation)
                session.commit()
            return conversation
    
    async def trim_message_history(self, user_session_key, company_id):
        with self.session_factory() as session:
            # Trim the message history by soft-deleting older messages if the response usage tokens exceed the limit
            conversation = await self.get_latest_conversation(user_session_key, company_id)
            messages = session.query(Message).filter(
                            Message.conversation_id == conversation.id
                                ).order_by(Message.created_at).all()
            # Soft delete all messages except the first one and the last two
            for i, message in enumerate(messages):
                if i == 0 or i >= len(messages) - 2:
                    continue  # Skip the first message and the last two messages
                message.is_deleted = True
            session.commit()
        return "Message History successfully trimmed"
            
    async def update_prompt_message(self, user_session_key, new_prompt:str, company_id:int):
        with self.session_factory() as session:
            # Get the latest conversation for the user
            conversation = await self.get_latest_conversation(user_session_key, company_id)            
            first_message = session.query(Message).filter(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at).first()
            # Update the content of the first message with the new prompt
            if first_message:
                first_message.content = new_prompt
                first_message.role = "system"
                session.commit()
            else:
                await self.insert_message(user_session_key=user_session_key,role='system', content=new_prompt, company_id=company_id)
        return "Prompt successfully updated"


    async def get_or_create_user(self, user_session_key, company_id:int)->ChatUser:
        # Implement the method to get or create a user
        with self.session_factory() as session:
            user = session.query(ChatUser).options(noload(ChatUser.company)).filter(ChatUser.user_session_key == user_session_key, ChatUser.company_id == company_id).first()
            if user is None:
                user = ChatUser(user_session_key=user_session_key
                                , company_id=company_id
                                , is_deleted = False)
                session.add(user)
                session.commit()
            return user
	

