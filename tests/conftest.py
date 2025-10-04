# global test settings
# fixtures, etc

from unittest.mock import patch

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models.base import DBase, DBSession
from fastapi.testclient import TestClient
from models.deps import get_db
from app import app

from models.employee import Employee, ESkill
from models.department import Department
from repositories.employee_repository import EmployeeRepository
from repositories.skills_repository import SkillRepository
from repositories.department_repository import DepartmentRepository


@pytest.fixture(scope="function")
def setup_employee(test_db):
    session = test_db()
    emp_repo = EmployeeRepository(session)
    employee = emp_repo.add(Employee(fname="test fname", lname="test lname"))
    return emp_repo, employee


@pytest.fixture(scope="function")
def setup_skill(test_db):
    session = test_db()
    skill_repo = SkillRepository(session)
    skill = skill_repo.add(ESkill(skill_name="testing skill"))
    return skill_repo, skill


@pytest.fixture(scope="function")
def setup_department(test_db):
    session = test_db()
    dept_repo = DepartmentRepository(session)
    department = dept_repo.add(Department("ramp"))
    return dept_repo, department


@pytest.fixture()
def test_client(test_db, name="test_client", scope="function"):
    with TestClient(app) as client:
        yield client


# @pytest.fixture()
# def test_db(name="test_db", scope="function"):
#     print("test db up")
#     db_engine = sa.create_engine("sqlite://")
#     TestingSessionLocal = sessionmaker(bind=db_engine, expire_on_commit=False)
#     DBSession.configure(bind=db_engine, expire_on_commit=False)
#     DBase.metadata.create_all(db_engine)

#     try:
#         yield
#     finally:
#         DBase.metadata.drop_all(db_engine)

#         print("test db connection closed")


@pytest.fixture(scope="function")
def test_db():
    print("test db up")

    db_engine = sa.create_engine(
        "sqlite://", connect_args={"check_same_thread": False})
    connection = db_engine.connect()

    DBase.metadata.create_all(connection)

    TestingSessionLocal = sessionmaker(bind=connection, expire_on_commit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    DBase.metadata.drop_all(connection)
    connection.close()
    app.dependency_overrides.clear()
    print("test db connection closed")
