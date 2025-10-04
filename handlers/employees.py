import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.employee import Employee
from models.schemas import EmployeeSchema
from models.deps import get_db
from repositories.employee_repository import EmployeeRepository
from repositories.skills_repository import SkillRepository
from repositories.department_repository import DepartmentRepository

router = APIRouter(prefix="/employees")


@router.get("/", tags=["employees"])
def get_employees(db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    employees = repo.get_all()
    return [e.as_dict() for e in employees]


@router.get("/{pk}", tags=["employees"])
def get_employee(pk: int, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    employee = repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.as_dict()


@router.post("/", tags=["employees"])
def create_employee(employeeItem: EmployeeSchema, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    employee = Employee(
        employeeItem.first_name,
        employeeItem.last_name
    )
    repo.add(employee)
    return employee.as_dict()


@router.put("/{pk}", tags=["employees"])
def update_employee(pk: int, employeeItem: EmployeeSchema, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    employee = repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    repo.update(employee, employeeItem)
    return employee.as_dict()


@router.delete("/{pk}", tags=["employees"])
def delete_employee(pk: int, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    employee = repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    repo.delete(employee)
    return {"ok": True}


@router.post("/{pk}/skill/{skill_pk}", tags=["employee_skill"])
def employee_add_skill(pk: int, skill_pk: int, db: Session = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    skills_repo = SkillRepository(db)
    employee = employee_repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill = skills_repo.get_by_id(skill_pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    employee_repo.add_skill(employee, skill)
    return employee.as_dict()


@router.delete("/{pk}/skill/{skill_pk}", tags=["employee_skill"])
def employee_delete_skill(pk: int, skill_pk: int, db: Session = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    skills_repo = SkillRepository(db)
    employee = employee_repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill = skills_repo.get_by_id(skill_pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    employee_repo.delete_skill(employee, skill)
    return employee.as_dict()


@router.post("/{pk}/department/{department_pk}", tags=["employee_department"])
def employee_add_department(pk: int, department_pk: int, db: Session = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    employee = employee_repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    department_repo = DepartmentRepository(db)
    department = department_repo.get_by_id(department_pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    employee_repo.set_department(employee, department)
    return employee.as_dict()


@router.delete("/{pk}/department/{department_pk}", tags=["employee_department"])
def employee_delete_department(pk: int, department_pk: int, db: Session = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    employee = employee_repo.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    department_repo = DepartmentRepository(db)
    department = department_repo.get_by_id(department_pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    employee_repo.delete_department(employee, department)
    return employee.as_dict()
