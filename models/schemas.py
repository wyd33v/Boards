from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    name: str


class SkillSchema(BaseModel):
    name: str


class EmployeeSchema(BaseModel):
    first_name: str
    last_name: str
