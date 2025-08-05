"""
A file that contains class of Employee and everything related.
"""
import uuid

from models.storage import Storage
from models.department import Department


class ESkill(Storage):
    file_path = "./data/skills"

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
        super().add() 
        print("skill was created") 
    
    @classmethod
    def get_all(cls):
        print(len(cls.storage))
        return cls.storage.items()

class Employee(Storage):
    file_path = "./data/employees"

    def __init__(self, fname, lname, position, department: Department):
        self.id = uuid.uuid1()
        self.first_name = fname
        self.last_name = lname
        self.position = position
        self.department = department
        self.skills = []
        super().add()
        print("employee was created") 

    def add_skill(self, skill: ESkill):
        self.skills.append(skill)

    def get_skills(self):
        # skills = []
        # for s in self.skills:
        #     skills.append(s.name)
        return [x.name for x in self.skills]

    def get_name(self):
        return self.first_name
    
    @classmethod
    def get_all(cls):
        print(len(cls.storage))
        return cls.storage.items()
    
    def check_skill(self, s):
        return s in self.skills
