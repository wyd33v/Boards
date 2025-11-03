from fastapi import APIRouter, Depends, HTTPException

from models.schemas import DepartmentSchema
from services import department_service, DepartmentService

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/")
def get_departments(service: DepartmentService = Depends(department_service)):
    departments = service.get_all_departments()
    return [d.as_dict() for d in departments]


@router.get("/{pk}")
def get_department(pk: int, service: DepartmentService = Depends(department_service)):
    department = service.get_department(pk)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.as_dict()


# @router.get("/by-name/{name}")
# def get_department_by_name(name: str, db: Session = Depends(get_session)):
#     repo = DepartmentRepository(db)
#     department = repo.get_by_name(name)
#     if department is None:
#         raise HTTPException(status_code=404, detail="Department not found")
#     return department.as_dict()


@router.post("/")
def create_department(
    department_item: DepartmentSchema,
    service: DepartmentService = Depends(department_service)
):
    department = service.create_department(department_item)
    return department.as_dict()


@router.put("/{pk}")
def update_department(
    pk: int,
    department_item: DepartmentSchema,
    service: DepartmentService = Depends(department_service)
):
    department = service.update_department(pk, department_item)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department.as_dict()


@router.delete("/{pk}")
def delete_department(pk: int, service: DepartmentService = Depends(department_service)):
    result = service.delete_department(pk)
    if not result:
        raise HTTPException(status_code=404, detail="Department not found")
    return result
