"""
A file that contains class of Department and everything related.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import DBase, db_session
from .schemas import DepartmentSchema


class Department(DBase):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship("Employee", back_populates='department')

    def __init__(self, department_name):
        self.name = department_name
        print("department was created")

    def __repr__(self):
        return f"department {self.id} {self.name}"

    def __str__(self):
        return f"{self.name}"

    def as_dict(self):
        dict_model = {
            "id": self.id,
            "name": self.name,
        }
        return dict_model

    def save(self):
        db_session.add(self)
        db_session.commit()
        return self.id

    def update(self, department: DepartmentSchema):
        self.name = department.name
        self.save()
        return self

    def delete(self):
        db_session.delete(self)
        db_session.commit()
        pass

    @classmethod
    def get_all(cls):
        result = db_session.query(cls).all()
        return result

    @classmethod
    def get_by_id(cls, pk):
        result = db_session.query(cls).get(pk)
        return result

    @classmethod
    def get_by_name(cls, name: str):
        return db_session.query(cls).filter(cls.name == name).one_or_none()
