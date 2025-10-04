import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from models.deps import get_db
from repositories.employee_repository import EmployeeRepository
from repositories.skills_repository import SkillRepository
from models.employee import ESkill
from models.schemas import SkillSchema

router = APIRouter(prefix="/skills")


@router.get("/", tags=["skills"])
def get_skills(db: Session = Depends(get_db)):
    repo = SkillRepository(db)
    skills = repo.get_all()
    return [s.as_dict() for s in skills]


@router.get("/{pk}", tags=["skills"])
def get_skill(pk: int, db: Session = Depends(get_db)):
    repo = SkillRepository(db)
    skill = repo.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill.as_dict()


@router.post("/", tags=["skills"])
def create_skills(skillItem: SkillSchema, db: Session = Depends(get_db)):
    repo = SkillRepository(db)
    skill = ESkill(skillItem.name)
    repo.add(skill)
    return skill.as_dict()


@router.put("/{pk}", tags=["skills"])
def update_skills(pk: int, skillItem: SkillSchema, db: Session = Depends(get_db)):
    repo = SkillRepository(db)
    skill = repo.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    repo.update(skill, skillItem)
    return skill.as_dict()


@router.delete("/{pk}", tags=["skills"])
def delete_skill(pk: int, db: Session = Depends(get_db)):
    repo = SkillRepository(db)
    skill = repo.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    repo.delete(skill)
    return {"ok": True}


@router.get("/{pk}/employees", tags=["employee_skill"])
def get_all_employees_by_skill(pk: int, db: Session = Depends(get_db)):
    repo = SkillRepository(db)
    employees = repo.get_employees_by_skill_id(pk)
    if employees is None:
        raise HTTPException(
            status_code=404, detail="Skill not found or no employees")

    return [e.as_dict() for e in employees]


@router.post("/{pk}/employees/{employee_pk}", tags=["employee_skill"])
def skill_add_employee(pk: int, employee_pk: int, db: Session = Depends(get_db)):
    skill_repo = SkillRepository(db)
    employee_repo = EmployeeRepository(db)

    skill = skill_repo.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    employee = employee_repo.get_by_id(employee_pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    skill_repo.add_employee(skill, employee)
    return employee.as_dict()


@router.delete("/{pk}/employee/{employee_pk}", tags=["employee_skill"])
def skill_delete_employee(pk: int, employee_pk: int, db: Session = Depends(get_db)):
    skill_repo = SkillRepository(db)
    employee_repo = EmployeeRepository(db)

    skill = skill_repo.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    employee = employee_repo.get_by_id(employee_pk)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    if skill not in employee.skills:
        raise HTTPException(
            status_code=404, detail="Employee does not have this skill")

    skill_repo.delete_employee(skill, employee)
    return employee.as_dict()
