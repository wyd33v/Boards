import json

from fastapi import APIRouter, HTTPException

from models.employee import Employee
from models.schemas import EmployeeSchema

router = APIRouter(prefix="/employees")

@router.get("/", tags=[""])
def get_employees():
    employees = Employee.get_all()

    return [e.as_dict() for e in employees]


@router.get("/{pk}", tags=[""])
def get_employee(pk: int):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee.as_dict()


@router.post("/", tags=[""])
def create_employee(employeeItem: EmployeeSchema):
    e = Employee(
            employeeItem.first_name, 
            employeeItem.last_name, 
            employeeItem.position, 
            employeeItem.department_id
        )
    
    e.save()
    return e.id

@router.put("/{pk}", tags=[""])
def update_skills(pk: int, employeeItem: EmployeeSchema):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")    
    employee.update(employeeItem)
    return employee.as_dict()

@router.delete("/{pk}", tags=[""])
def delete_skill(pk:int):
    employee = Employee.get_by_id(pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")   
    employee.delete()
    return {"ok": True}    

