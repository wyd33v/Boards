# global test settings 
# fixtures, etc

from unittest.mock import patch

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session, declarative_base

from models.base import DBase
from models.department import Department
from models.employee import Employee, EmployeeSkills, ESkill


@pytest.fixture()
def test_db(name="test_db", scope="function"):
    with patch("models.department.db_session") as f:
        try:
            db_engine = sa.create_engine('sqlite://',echo=True)
            db_conn = db_engine.connect()
            db_session = Session(db_engine)
            DBase.metadata.create_all(db_engine)
            print("test db up")
            yield db_session
        finally:
            DBase.metadata.drop_all(db_engine)
            db_conn.close()
            print("test db connection closed")
