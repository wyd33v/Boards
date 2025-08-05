import sys

sys.path.append(".")

import uuid 

from models.department import Department
from models.employee import Employee
from models.employee import ESkill

Department.initialize_storage()
Employee.initialize_storage()
ESkill.initialize_storage()

#Department
def create_and_dump_departments():
    ramp = Department("ramp")
    tech = Department("tech")  
    print(ramp.id)
    print(Department.get_all())
    Department.dump_data()


def load_dumped_departments():
    Department.load_data()
    print(Department.get_all())
    
#Employee
def create_and_dump_employee():
    Department.load_data()
    id = uuid.UUID('faf01653-65b2-4224-98b3-0ff8a88cded5')

    employee1 = Employee("Bruce", "Wayne", "CEO", Department.get(id)) 
    Employee.dump_data()

def load_dumped_employees():
    Employee.load_data()
    print(Employee.get_all())

#Skills
def create_and_dump_skill():
    skill = ESkill("ramp leader") 
    ESkill.dump_data()

def load_dumped_skills():
    ESkill.load_data()
    print(ESkill.get_all())

def employee_add_new_skill():
    Employee.load_data()
    ESkill.load_data()
    employee_id = uuid.UUID('7b622810-722c-11f0-b8ee-b42e9960d092')
    skill_id = uuid.UUID('63b4f8c6-722d-11f0-8ecf-b42e9960d092')
   
    employee = Employee.get(employee_id)
    skill = ESkill.get(skill_id)
    print(skill.name)
    employee.add_skill(skill)

    print(employee.get_skills)

#def get_employee_skills()
    


if __name__ == "__main__":
    #create_and_dump_departments()
    
    #load_dumped_departments()

    #create_and_dump_employee()
    #load_dumped_employees()

    #create_and_dump_skill()
    #load_dumped_skills()
    
    employee_add_new_skill()
