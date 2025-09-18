import sqlalchemy as sa
from sqlalchemy.orm import Session, declarative_base

from config import Config

db_engine = sa.create_engine(f"sqlite:///{Config.DB_PATH}")
db_session = Session(db_engine)
DBase = declarative_base()
