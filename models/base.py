import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Config

db_engine = sa.create_engine(f"sqlite:///{Config.DB_PATH}")
DBase = declarative_base()
DBSession = sessionmaker(bind=db_engine, expire_on_commit=False)
