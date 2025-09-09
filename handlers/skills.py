import json

from fastapi import APIRouter, HTTPException

from models.employee import ESkill
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


@router.post("/{pk}/employee/{employee_pk}", tags=["employee_skill"])
def skill_add_employee(pk: int, employee_pk: int):
    # TODO: call class method
    return {"pk": pk, "employee_pk": employee_pk}


@router.delete("/{pk}/employee/{employee_pk}", tags=["employee_skill"])
def skill_delete_employee(pk: int, employee_pk: int):
    # TODO: call class method
    return {"pk": pk, "employee_pk": employee_pk}
