from fastapi import Depends
from sqlalchemy.orm import Session
from models.deps import get_session
from services.department_service import DepartmentService
from services.employee_service import EmployeeService
from services.skills_service import SkillsService


def get_department_service(db: Session = Depends(get_session)) -> DepartmentService:
    return DepartmentService(db)


def get_skills_service(db: Session = Depends(get_session)) -> SkillsService:
    return SkillsService(db)


def get_employee_service(db: Session = Depends(get_session)) -> EmployeeService:
    return EmployeeService(db)
