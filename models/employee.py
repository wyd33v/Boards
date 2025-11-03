"""
A file that contains class of Employee and everything related.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from .base import DBase


class ESkill(DBase):
    __tablename__ = "eskills"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship(
        "Employee", secondary='employee_skills', back_populates='skills')

    def __init__(self, skill_name):
        self.name = skill_name

    def __repr__(self):
        return f"skill {self.id} {self.name}"

    def __str__(self):
        return f"{self.name}"

    def as_dict(self):
        dict_model = {
            "id": self.id,
            "name": self.name,
        }
        return dict_model


class Employee(DBase):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    department_id = mapped_column(ForeignKey("departments.id"))
    department = relationship(
        "Department", back_populates="employees", lazy="subquery")
    skills = relationship(
        "ESkill", secondary='employee_skills', lazy='immediate')

    def __init__(self, fname, lname):
        self.first_name = fname
        self.last_name = lname
        
    def __repr__(self):
        return f"employee {self.id} {self.first_name} {self.first_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.skills}"

    def as_dict(self):
        dict_model = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "department": self.department,
            "skills": [s.as_dict() for s in self.skills],
        }
        return dict_model


class EmployeeSkills(DBase):
    __tablename__ = "employee_skills"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    skill_id = Column(Integer, ForeignKey('eskills.id'))


# class EmployeeDepartment(DBase):
#     __tablename__ = "employee_department"

#     id = Column(Integer, primary_key=True)
#     employee_id = Column(Integer, ForeignKey('employees.id'))
#     department_id = Column(Integer, ForeignKey('departments.id'))
