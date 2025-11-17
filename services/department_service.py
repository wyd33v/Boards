from sqlalchemy.orm import Session

from data.repository import Repository
from models.department import Department
from models.schemas import DepartmentSchema


class DepartmentService:
    def __init__(self, db: Session):
        self.repo = Repository(Department, db)

    def get_all_departments(self):
        departments = self.repo.get_all()
        return departments

    def get_department(self, pk: int):
        department = self.repo.get_by_id(pk)
        if not department:
            return None
        return department

    def create_department(self, department_item: DepartmentSchema):
        department = Department(department_name=department_item.name)
        saved = self.repo.save(department)
        return saved

    def update_department(self, pk: int, department_item: DepartmentSchema):
        department = self.repo.get_by_id(pk)
        if not department:
            return None
        department.name = department_item.name
        self.repo.save(department)
        return department

    def delete_department(self, pk: int):
        department = self.repo.get_by_id(pk)
        if not department:
            return None
        self.repo.delete(department)
        return {"ok": True}  # TODO
