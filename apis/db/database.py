from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..db_models.model import Base

DATABASE_URL = 'sqlite:///test.sqlite'

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)
