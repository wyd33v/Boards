"""
A file that contains class of Department and everything related.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import DBase


class Department(DBase):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship("Employee", back_populates="department")

    def __init__(self, department_name: str):
        self.name = department_name

    def __repr__(self):
        return f"department {self.id} {self.name}"

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
