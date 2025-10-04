from sqlalchemy.orm import Session
from models.department import Department
from models.schemas import DepartmentSchema


class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, department: Department) -> Department:
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department

    def update(self, department: Department, data: DepartmentSchema) -> Department:
        department.name = data.name
        self.db.commit()
        self.db.refresh(department)
        return department

    def delete(self, department: Department):
        self.db.delete(department)
        self.db.commit()

    def get_all(self) -> list[Department]:
        return self.db.query(Department).all()

    def get_by_id(self, pk: int) -> Department | None:
        return self.db.query(Department).get(pk)

    def get_by_name(self, name: str) -> Department | None:
        return self.db.query(Department).filter(Department.name == name).one_or_none()
