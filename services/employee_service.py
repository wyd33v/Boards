from sqlalchemy.orm import Session

from data.repository import Repository
from models.department import Department
from models.employee import Employee, ESkill
from models.schemas import EmployeeSchema


class EmployeeService:
    def __init__(self, db: Session):
        self.repo = Repository(Employee, db)

    def get_all_employees(self):
        employees = self.repo.get_all()
        return employees

    def get_employee(self, pk: int):
        employee = self.repo.get_by_id(pk)
        if not employee:
            return None
        return employee

    def create_employee(self, employee_item: EmployeeSchema):
        employee = Employee(
            fname=employee_item.first_name, lname=employee_item.last_name
        )
        saved = self.repo.save(employee)
        return saved

    def update_employee(self, pk: int, employee_item: EmployeeSchema):
        employee = self.repo.get_by_id(pk)
        if not employee:
            return None
        employee.first_name = employee_item.first_name
        employee.last_name = employee_item.last_name
        self.repo.save(employee)
        return employee

    def delete_employee(self, pk: int):
        employee = self.repo.get_by_id(pk)
        if not employee:
            return None
        self.repo.delete(employee)
        return {"ok": True}

    def add_skill_to_employee(self, employee: Employee, skill: ESkill):
        employee.skills.append(skill)
        self.repo.save(employee)
        return employee

    def remove_skill_from_employee(self, employee: Employee, skill: ESkill):
        employee.skills.remove(skill)
        self.repo.save(employee)
        return employee

    def set_department_for_employee(
        self, employee: Employee, department: Department
    ) -> Employee:
        employee.department = department
        self.repo.save(employee)
        return employee

    def delete_department_from_employee(self, employee: Employee) -> Employee:
        employee.department = None
        self.repo.save(employee)
        return employee
