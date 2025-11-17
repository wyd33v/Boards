from sqlalchemy.orm import Session

from data.repository import Repository
from models.employee import Employee, ESkill
from models.schemas import SkillSchema


class SkillsService:
    def __init__(self, db: Session):
        self.repo = Repository(ESkill, db)

    def get_all_skills(self):
        skills = self.repo.get_all()
        return skills

    def get_skill(self, pk: int):
        skill = self.repo.get_by_id(pk)
        if not skill:
            return None
        return skill

    def create_skill(self, skill_item: SkillSchema):
        skill = ESkill(skill_name=skill_item.name)
        saved = self.repo.save(skill)
        return saved

    def update_skill(self, pk: int, skill_item: SkillSchema):
        skill = self.repo.get_by_id(pk)
        if not skill:
            return None
        skill.name = skill_item.name
        self.repo.save(skill)
        return skill

    def delete_skill(self, pk: int):
        skill = self.repo.get_by_id(pk)
        if not skill:
            return None
        self.repo.delete(skill)
        return {"ok": True}

    def add_employee_to_skill(self, skill: ESkill, employee: Employee):
        skill.employees.append(employee)
        self.repo.save(skill)
        return skill

    def remove_employee_from_skill(self, skill: ESkill, employee: Employee):
        skill.employees.remove(employee)
        self.repo.save(skill)
        return skill
