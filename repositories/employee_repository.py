from sqlalchemy.orm import Session
from models.employee import Employee, ESkill
from models.department import Department
from models.schemas import EmployeeSchema  


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update(self, employee: Employee, data: EmployeeSchema) -> Employee:
        employee.first_name = data.first_name
        employee.last_name = data.last_name
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: Employee):
        self.db.delete(employee)
        self.db.commit()

    def get_all(self) -> list[Employee]:
        return self.db.query(Employee).all()

    def get_by_id(self, pk: int) -> Employee | None:
        return self.db.query(Employee).get(pk)

    def add_skill(self, employee: Employee, skill: ESkill) -> Employee:
        employee.skills.append(skill)
        self.db.commit()
        self.db.refresh(employee)  #???
        return employee

    def delete_skill(self, employee: Employee, skill: ESkill) -> Employee:
        employee.skills.remove(skill)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def set_department(self, employee: Employee, department: Department) -> Employee:
        employee.department = department
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete_department(self, employee: Employee) -> Employee:
        employee.department = None
        self.db.commit()
        self.db.refresh(employee)
        return employee
