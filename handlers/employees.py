
from fastapi import APIRouter, Depends, HTTPException

from models.schemas import EmployeeSchema
from services import (department_service,
                      employee_service, skills_service, DepartmentService, EmployeeService, SkillsService)

router = APIRouter(prefix="/employees")


@router.get("/", tags=["employees"])
def get_employees(service: EmployeeService = Depends(employee_service)):
    employees = service.get_all_employees()
    return [e.as_dict() for e in employees]


@router.get("/{pk}", tags=["employees"])
def get_employee(pk: int, service: EmployeeService = Depends(employee_service)):
    employee = service.get_employee(pk)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.as_dict()


@router.post("/", tags=["employees"])
def create_employee(employee_item: EmployeeSchema, service: EmployeeService = Depends(employee_service)):
    employee = service.create_employee(employee_item)
    return employee.as_dict()


@router.put("/{pk}", tags=["employees"])
def update_employee(
    pk: int,
    employee_item: EmployeeSchema,
    service: EmployeeService = Depends(employee_service)
):
    employee = service.update_employee(pk, employee_item)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.as_dict()


@router.delete("/{pk}", tags=["employees"])
def delete_employee(pk: int, service: EmployeeService = Depends(employee_service)):
    result = service.delete_employee(pk)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result


@router.post("/{pk}/skill/{skill_pk}", tags=["employee_skill"])
def employee_add_skill(
    pk: int,
    skill_pk: int,
    skill_service: SkillsService = Depends(skills_service),
    employee_service: EmployeeService = Depends(employee_service)
):
    employee = employee_service.get_employee(pk)
    skill = skill_service.get_skill(skill_pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    if skill in employee.skills:
        return employee.as_dict()

    employee = employee_service.add_skill_to_employee(employee, skill)
    return employee.as_dict()


@router.delete("/{pk}/skill/{skill_pk}", tags=["employee_skill"])
def employee_delete_skill(
    pk: int,
    skill_pk: int,
    skill_service: SkillsService = Depends(skills_service),
    employee_service: EmployeeService = Depends(employee_service)
):
    employee = employee_service.get_employee(pk)
    skill = skill_service.get_skill(skill_pk)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    employee = employee_service.remove_skill_from_employee(employee, skill)
    return employee.as_dict()


@router.post("/{pk}/department/{department_pk}", tags=["employee_department"])
def employee_add_department(
    pk: int,
    department_pk: int,
    department_service: DepartmentService = Depends(department_service),
    employee_service: EmployeeService = Depends(employee_service)
):
    employee = employee_service.get_employee(pk)
    department = department_service.get_department(department_pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    if employee.department == department:
        return employee.as_dict()

    employee = employee_service.set_department_for_employee(
        employee, department)
    return employee.as_dict()


@router.delete("/{pk}/department", tags=["employee_department"])
def employee_delete_department(
    pk: int,
    # department_pk: int,
    # department_service: DepartmentService = Depends(department_service),
    employee_service: EmployeeService = Depends(employee_service)
):
    employee = employee_service.get_employee(pk)
    # department = department_service.get_department(department_pk)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # if department is None:
    #     raise HTTPException(status_code=404, detail="Department not found")

    # if employee.department == department:
    #     return employee.as_dict()

    employee = employee_service.delete_department_from_employee(employee)
    return employee.as_dict()
