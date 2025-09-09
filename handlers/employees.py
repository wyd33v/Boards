import json

from fastapi import APIRouter, HTTPException

from handlers import skills
from models.employee import Employee, ESkill
from models.schemas import EmployeeSchema

router = APIRouter(prefix="/employees")

@router.get("/", tags=["employees"])
def get_employees():
    employees = Employee.get_all()

    return [e.as_dict() for e in employees]


@router.get("/{pk}", tags=["employees"])
def get_employee(pk: int):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.as_dict()


@router.post("/", tags=["employees"])
def create_employee(employeeItem: EmployeeSchema):
    e = Employee(
            employeeItem.first_name, 
            employeeItem.last_name, 
            employeeItem.position, 
            employeeItem.department_id
        )
    
    e.save()
    return e.id

@router.put("/{pk}", tags=["employees"])
def update_skills(pk: int, employeeItem: EmployeeSchema):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")    
    employee.update(employeeItem)
    return employee.as_dict()

@router.delete("/{pk}", tags=["employees"])
def delete_skill(pk:int):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")   
    employee.delete()
    return {"ok": True}



@router.post("/{pk}/skill/{skill_pk}", tags=["employee_skill"])
def employee_add_skill(pk:int, skill_pk: int):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found") 
    s = ESkill.get_by_id(skill_pk)
    if s is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    employee.add_skill(s)
    return employee.as_dict()

@router.delete("/{pk}/skill/{skill_pk}", tags=["employee_skill"])
def employee_delete_skill(pk:int, skill_pk: int):
    s = ESkill.get_by_id(skill_pk)
    if s is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"pk": pk, "skill": str(s)}
