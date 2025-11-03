from models.base import db_session
from .department_service import DepartmentService
from .employee_service import EmployeeService
from .skills_service import SkillsService


def department_service() -> DepartmentService:
    return DepartmentService(db_session())


def skills_service() -> SkillsService:
    return SkillsService(db_session())


def employee_service() -> EmployeeService:
    return EmployeeService(db_session())
