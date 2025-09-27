# global test settings 
# fixtures, etc

from unittest.mock import patch

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session, declarative_base

from models.base import DBase, DBSession
from models.department import Department
from models.employee import Employee, EmployeeSkills, ESkill


@pytest.fixture()
def test_db(name="test_db", scope="function"):
    print("test db up")
    db_engine = sa.create_engine("sqlite://")
    DBSession.configure(bind=db_engine, expire_on_commit=False)
    DBase.metadata.create_all(db_engine)
    try:
        yield
    finally:
        DBase.metadata.drop_all(db_engine)
        print("test db connection closed")
