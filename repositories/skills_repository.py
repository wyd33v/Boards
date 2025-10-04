from sqlalchemy.orm import Session
from models.employee import Employee, ESkill
from models.schemas import SkillSchema


class SkillRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, skill: ESkill) -> ESkill:
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def update(self, skill: ESkill, data: SkillSchema) -> ESkill:
        skill.name = data.name
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def delete(self, skill: ESkill):
        self.db.delete(skill)
        self.db.commit()

    def get_all(self) -> list[ESkill]:
        return self.db.query(ESkill).all()

    def get_by_id(self, pk: int) -> ESkill | None:
        return self.db.query(ESkill).get(pk)

    def get_by_name(self, name: str) -> ESkill | None:
        return self.db.query(ESkill).filter(ESkill.name == name).one_or_none()

    def get_employees_by_skill_id(self, skill_id: int) -> list[Employee]:
        skill = self.db.query(ESkill).get(skill_id)
        if skill is None:
            return []
        return skill.employees

    def add_employee(self, skill: ESkill, employee: Employee) -> ESkill:
        skill.employees.append(employee)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def delete_employee(self, skill: ESkill, employee: Employee) -> ESkill:
        skill.employees.remove(employee)
        self.db.commit()
        self.db.refresh(skill)
        return skill
