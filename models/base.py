import sqlalchemy as sa
from sqlalchemy.orm import Session, declarative_base

from config import Config

DBase = declarative_base()

db_engine = sa.create_engine(f"sqlite:///{Config.DB_PATH}")
db_conn = db_engine.connect()
db_session = Session(db_engine)
