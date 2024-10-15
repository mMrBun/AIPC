from sqlalchemy import Column, Integer, String, DateTime, func, Text, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MessageCard(Base):
    __tablename__ = 'message_card'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    create_datetime = Column(String, nullable=False, default=func.strftime('%Y-%m-%d %H:%M:%S',func.now()))

class ChatMessage(Base):
    __tablename__ = 'chat_message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    history_content = Column(Text, nullable=False)
    message_card_id = Column(Integer, nullable=False, index=True)
    create_datetime = Column(String, nullable=False, default=func.strftime('%Y-%m-%d %H:%M:%S',func.now()))

class AssistantCard(Base):
    __tablename__ = 'assistant_card'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    # create_datetime = Column(String, nullable=False, default=func.strftime('%Y-%m-%d %H:%M:%S',func.now()))