import json

from fastapi import APIRouter, HTTPException

from models.department import Department 
from models.schemas import DepartmentSchema

router = APIRouter(prefix="/department")

@router.get("/", tags=[""])
def get_departments():
    departments = Department.get_all()

    return [d.as_dict() for d in departments]


@router.get("/{pk}", tags=[""])
def get_department(pk: int):
    department = Department.get_by_id(pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.as_dict()


@router.post("/", tags=[""])
def create_department(departmentItem: DepartmentSchema):
    department = Department(
            departmentItem.name
        )    
    department.save()
    return department.id

@router.put("/{pk}", tags=[""])
def update_department(pk: int, departmentItem: DepartmentSchema):
    department = Department.get_by_id(pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")    
    department.update(departmentItem)
    return department.as_dict()

@router.delete("/{pk}", tags=[""])
def delete_department(pk:int):
    department = Department.get_by_id(pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")   
    department.delete()
    return {"ok": True}    

