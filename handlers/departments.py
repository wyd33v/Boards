from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.department import Department
from models.schemas import DepartmentSchema
from models.deps import get_db
from repositories.department_repository import DepartmentRepository

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    departments = repo.get_all()
    return [d.as_dict() for d in departments]


@router.get("/{pk}")
def get_department(pk: int, db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    department = repo.get_by_id(pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.as_dict()


@router.get("/by-name/{name}")
def get_department_by_name(name: str, db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    department = repo.get_by_name(name)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.as_dict()


@router.post("/")
def create_department(department_item: DepartmentSchema, db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    department = Department(department_name=department_item.name)
    repo.add(department)
    return department.as_dict()


@router.put("/{pk}")
def update_department(pk: int, department_item: DepartmentSchema, db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    department = repo.get_by_id(pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    repo.update(department, department_item)
    return department.as_dict()


@router.delete("/{pk}")
def delete_department(pk: int, db: Session = Depends(get_db)):
    repo = DepartmentRepository(db)
    department = repo.get_by_id(pk)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    repo.delete(department)
    return {"ok": True}
