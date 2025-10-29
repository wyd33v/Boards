from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import Config

db_engine = create_engine(f"sqlite:///{Config.DB_PATH}")
DBase = declarative_base()
DBSession = sessionmaker(bind=db_engine, expire_on_commit=False)


def db_session():
    with Session(db_engine) as session:
        yield session
