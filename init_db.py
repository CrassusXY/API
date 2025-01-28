from db import Base, engine
from models import Message

_initialized = False

def init_db_once():
    global _initialized
    if _initialized:
        return
    print("creating 'messages' if it dont exist...")
    Base.metadata.create_all(engine)
    print("Database ready!")
    _initialized = True
