import json

from fastapi import APIRouter, HTTPException

from models.employee import ESkill
from models.schemas import SkillSchema

router = APIRouter(prefix="/skills")


@router.get("/", tags=[""])
def get_skills():
    skills = ESkill.get_all()

    return [skill.as_dict() for skill in skills]


@router.get("/{pk}", tags=[""])
def get_skill(pk: int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return skill.as_dict()


@router.post("/", tags=[""])
def create_skills(skillItem: SkillSchema):
    s = ESkill(skillItem.name)
    s.save()
    return s.id

@router.put("/{pk}", tags=[""])
def update_skills(pk: int, skillItem: SkillSchema):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")    
    skill.update(skillItem)
    return skill.as_dict()

@router.delete("/{pk}", tags=[""])
def delete_skill(pk:int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")   
    skill.delete()
    return {"ok": True}    

