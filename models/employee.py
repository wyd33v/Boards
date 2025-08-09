"""
A file that contains class of Employee and everything related.
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from models.department import Department

from .base import DBase


class ESkill(DBase):
    __tablename__ = "eskills"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship("Employee", secondary='employee_skills', back_populates='skills')

    def __init__(self, skill_name):
        self.name = skill_name
        print("skill was created")
        
    def __repr__(self):
        return f"skill {self.id} {self.name}"
    
    def __str__(self):
        return f"{self.name}"

    # @classmethod
    # def get_all(cls):
    #     print(len(cls.storage))
    #     return cls.storage.items()

class Employee(DBase):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    position = Column(String)
    department_id = mapped_column(ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")
    skills = relationship("ESkill", secondary='employee_skills', back_populates='employees')

    def __init__(self, fname, lname, position, department: Department):
        self.first_name = fname
        self.last_name = lname
        self.position = position
        self.department = department
        print("employee was created")
        
    def __repr__(self):
        return f"employee {self.id} {self.first_name} {self.first_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.position}"

    # def add_skill(self, skill: ESkill):
    #     self.skills.append(skill)

    # def get_skills(self):
    #     # skills = []
    #     # for s in self.skills:
    #     #     skills.append(s.name)
    #     return [x.name for x in self.skills]

    # def check_skill(self, s):
    #     return s in self.skills



    



class EmployeeSkills(DBase):
    __tablename__ = "employee_skills"
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    skill_id = Column(Integer, ForeignKey('eskills.id'))
