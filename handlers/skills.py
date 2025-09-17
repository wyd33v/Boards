import json

from fastapi import APIRouter, HTTPException

from models.employee import ESkill, Employee, EmployeeSkills
from models.schemas import SkillSchema

router = APIRouter(prefix="/skills")


@router.get("/", tags=["skills"])
def get_skills():
    skills = ESkill.get_all()

    return [skill.as_dict() for skill in skills]


@router.get("/{pk}", tags=["skills"])
def get_skill(pk: int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return skill.as_dict()


@router.post("/", tags=["skills"])
def create_skills(skillItem: SkillSchema):
    s = ESkill(skillItem.name)
    s.save()
    return s.id


@router.put("/{pk}", tags=["skills"])
def update_skills(pk: int, skillItem: SkillSchema):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")
    skill.update(skillItem)
    return skill.as_dict()


@router.delete("/{pk}", tags=["skills"])
def delete_skill(pk: int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")
    skill.delete()
    return {"ok": True}


@router.get("/{pk}/employees", tags=["employee_skill"])
def get_all_employees_by_skill(pk: int):
    employees = ESkill.get_employee_by_skill_id(pk)

    return employees


@router.post("/{pk}/employees/{employee_pk}", tags=["employee_skill"])
def skill_add_employee(pk: int, employee_pk: int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    employee = Employee.get_by_id(employee_pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    skill.add_employee(employee)
    return employee.as_dict()


@router.delete("/{pk}/employee/{employee_pk}", tags=["employee_skill"])
def skill_delete_employee(pk: int, employee_pk: int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    employee = Employee.get_by_id(employee_pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not employee.check_skill(skill):
        raise HTTPException(
            status_code=404, detail="There is no employee with this skill")

    skill.delete_employee(employee)
    return employee.as_dict()
