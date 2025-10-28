from models.base import DBSession


def get_session():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
