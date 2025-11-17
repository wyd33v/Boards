from fastapi import APIRouter, Depends, HTTPException

from models.schemas import SkillSchema
from services import EmployeeService, SkillsService, employee_service, skills_service

router = APIRouter(prefix="/skills")


@router.get("/", tags=["skills"])
def get_skills(service: SkillsService = Depends(skills_service)):
    skills = service.get_all_skills()
    return [s.as_dict() for s in skills]


@router.get("/{pk}", tags=["skills"])
def get_skill(pk: int, service: SkillsService = Depends(skills_service)):
    skill = service.get_skill(pk)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.as_dict()


@router.post("/", tags=["skills"])
def create_skill(
    skill_item: SkillSchema, service: SkillsService = Depends(skills_service)
):
    skill = service.create_skill(skill_item)
    return skill.as_dict()


@router.put("/{pk}", tags=["skills"])
def update_skill(
    pk: int, skill_item: SkillSchema, service: SkillsService = Depends(skills_service)
):
    skill = service.update_skill(pk, skill_item)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.as_dict()


@router.delete("/{pk}", tags=["skills"])
def delete_skill(pk: int, service: SkillsService = Depends(skills_service)):
    result = service.delete_skill(pk)
    if not result:
        raise HTTPException(status_code=404, detail="Skill not found")
    return result


@router.get("/{pk}/employees", tags=["employee_skill"])
def get_all_employees_by_skill(
    pk: int, service: SkillsService = Depends(skills_service)
):
    skill = service.get_skill(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return [e.as_dict() for e in skill.employees]


@router.post("/{pk}/employees/{employee_pk}", tags=["employee_skill"])
def skill_add_employee(
    pk: int,
    employee_pk: int,
    skill_service: SkillsService = Depends(skills_service),
    employee_service: EmployeeService = Depends(employee_service),
):
    skill = skill_service.get_skill(pk)
    employee = employee_service.get_employee(employee_pk)

    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if employee in skill.employees:
        return employee.as_dict()

    skill = skill_service.add_employee_to_skill(skill, employee)
    return employee.as_dict()


@router.delete("/{pk}/employee/{employee_pk}", tags=["employee_skill"])
def skill_delete_employee(
    pk: int,
    employee_pk: int,
    skill_service: SkillsService = Depends(skills_service),
    employee_service: EmployeeService = Depends(employee_service),
):
    skill = skill_service.get_skill(pk)
    employee = employee_service.get_employee(employee_pk)

    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill = skill_service.remove_employee_from_skill(skill, employee)
    return employee.as_dict()
