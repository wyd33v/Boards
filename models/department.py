"""
A file that contains class of Department and everything related.
"""

from sqlalchemy import Column, Integer, String

from .base import DBase


class Department(DBase):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, department_name):
        self.name = department_name
        print("department was created")

    def __repr__(self):
        return f"department {self.id} {self.name}"

    def __str__(self):
        return f"{self.name}"
