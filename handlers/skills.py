import json

from fastapi import APIRouter, HTTPException

from models.employee import ESkill

router = APIRouter(prefix="/skills")


@router.get("/", tags=[""])
def get_skills():
    skills = ESkill.get_all()
    result = []
    
    for s in skills:
        print(s)
        result.append(s.name)

    return result


@router.get("/{pk}", tags=[""])
def get_skill(pk: int):
    skill = ESkill.get_by_id(pk)
    if skill is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return skill.as_dict()


@router.post("/", tags=[""])
def create_skills(name):
    s = ESkill(skill_name=name)
    s.save()
    return s.id

@router.put("/{pk}", tags=[""])
def create_skills(pk, name):
    pass

@router.delete("/{pk}", tags=[""])
def delete_skill(pk:int):
    pass
