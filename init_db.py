from db import Base, engine
from models import Message

_initialized = False

def init_db_once():
    global _initialized
    if _initialized:
        return
    print("Tworzę tabelę 'messages' jeśli nie istnieje...")
    Base.metadata.create_all(engine)
    print("✅ Tabela 'messages' gotowa!")
    _initialized = True
