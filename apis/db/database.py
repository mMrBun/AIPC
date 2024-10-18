import os
from typing import List, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..db_models.model import (
AssistantCard,
MessageCard,
ChatMessage,
)

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.sqlite')

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def new_chat(title: str) -> int:
    with Session() as session:
        message_card = MessageCard(title=title)
        session.add(message_card)
        session.commit()
        return message_card.id


def get_chat_by_name(title: str) -> list[Type[MessageCard]]:
    with Session() as session:
        message_cards = session.query(MessageCard).filter(MessageCard.title.like(f'%{title}%')).all()
        return message_cards

def get_all_chats() -> list[Type[MessageCard]]:
    with Session() as session:
        message_cards = session.query(MessageCard).all()
        return message_cards

def delete_chat(_id: int) -> None:
    with Session() as session:
        chat = session.query(MessageCard).filter(MessageCard.id == _id).first()
        if chat:
            session.delete(chat)
            session.query(ChatMessage).filter(ChatMessage.message_card_id == _id).delete(synchronize_session=False)
            session.commit()




def new_chat_message(message_card_id: int, history_content: str) -> int:
    with Session() as session:
        chat_message = ChatMessage(message_card_id=message_card_id, history_content=history_content)
        session.add(chat_message)
        session.commit()
        return chat_message.id


def get_chat_messages_by_chat_id(message_card_id: int) -> Type[ChatMessage]:
    with Session() as session:
        chat_messages = session.query(ChatMessage).filter(ChatMessage.message_card_id == message_card_id).first()
        return chat_messages

def new_assistant_card(title: str, description: str, content: str) -> int:
    with Session() as session:
        assistant_card = AssistantCard(title=title, description=description, content=content)
        session.add(assistant_card)
        session.commit()
        return assistant_card.id


def get_all_assistant_cards() -> list[Type[AssistantCard]]:
    with Session() as session:
        assistant_cards = session.query(AssistantCard).all()
        return assistant_cards


def get_assistant_card_by_id(assistant_card_id: int) -> Type[AssistantCard]:

    with Session() as session:
        assistant_card = session.query(AssistantCard).filter(AssistantCard.id == assistant_card_id).first()
        return assistant_card


