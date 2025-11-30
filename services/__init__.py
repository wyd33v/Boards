from models.base import db_session

from .cache_service import CacheService
from .department_service import DepartmentService
from .employee_service import EmployeeService
from .skills_service import SkillsService


def department_service() -> DepartmentService:
    return DepartmentService(db_session())


def skills_service() -> SkillsService:
    return SkillsService(db_session())


def employee_service() -> EmployeeService:
    return EmployeeService(db_session())

def cache_service() -> CacheService:
    return CacheService()
