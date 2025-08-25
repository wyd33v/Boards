from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    first_name: str
    last_name: str
    position: str
    department_id: int    

class SkillSchema(BaseModel):
    name: str
    
class DepartmentSchema(BaseModel):
    name: str 