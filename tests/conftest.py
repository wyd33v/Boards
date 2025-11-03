# global test settings
# fixtures, etc
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models.base import DBase, db_session
from services.department_service import DepartmentService
from services.employee_service import EmployeeService
from services.skills_service import SkillsService


@pytest.fixture
def fake_db():
    return MagicMock()


@pytest.fixture
def mock_repo():
    with patch("services.department_service.Repository") as mock_dept_repo_class, \
            patch("services.employee_service.Repository") as mock_emp_repo_class, \
            patch("services.skills_service.Repository") as mock_skills_repo_class:

        mock_dept_repo = MagicMock()
        mock_emp_repo = MagicMock()
        mock_skills_repo = MagicMock()

        mock_dept_repo_class.return_value = mock_dept_repo
        mock_emp_repo_class.return_value = mock_emp_repo
        mock_skills_repo_class.return_value = mock_skills_repo

        yield {
            "department": mock_dept_repo,
            "employee": mock_emp_repo,
            "skills": mock_skills_repo
        }


@pytest.fixture
def department_service(fake_db, mock_repo):
    return DepartmentService(fake_db)


@pytest.fixture
def employee_service(fake_db, mock_repo):
    return EmployeeService(fake_db)


@pytest.fixture
def skills_service(fake_db, mock_repo):
    return SkillsService(fake_db)


@pytest.fixture()
def test_client(test_db, name="test_client", scope="function"):
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    DBase.metadata.create_all(bind=engine)
    print("Test DB created")

    def override_db_session():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[db_session] = override_db_session

    db = TestingSessionLocal()
    yield db

    db.close()
    DBase.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()
    print("test db connection closed")
