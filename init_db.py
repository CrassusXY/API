from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    raw_data = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("✅ Tabela 'messages' została utworzona.")
