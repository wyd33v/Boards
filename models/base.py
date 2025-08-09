import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from config import Config

DBase = declarative_base()

engine = sa.create_engine(f"sqlite:///{Config.DB_PATH}")



print(engine)
print()
print()

db_conn = engine.connect() 
