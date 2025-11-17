from models.department import Department
from models.employee import Employee, ESkill

# ----------------------------
# Tests for ESkill
# ----------------------------


def test_eskill_init_and_attributes():
    skill = ESkill("Python")

    assert skill.name == "Python"
    assert skill.id is None


def test_eskill_repr_and_str():
    skill = ESkill("Java")
    skill.id = 1

    assert repr(skill) == "skill 1 Java"
    assert str(skill) == "Java"


def test_eskill_as_dict():
    skill = ESkill("Go")
    skill.id = 5

    expected = {"id": 5, "name": "Go"}
    assert skill.as_dict() == expected


# ----------------------------
# Tests for Employee
# ----------------------------


def test_employee_init_and_attributes():
    emp = Employee("John", "Doe")

    assert emp.first_name == "John"
    assert emp.last_name == "Doe"
    assert emp.id is None
    assert emp.department is None
    assert emp.skills == []


def test_employee_repr_and_str():
    emp = Employee("Jane", "Smith")
    emp.id = 1
    emp.skills = []

    assert repr(emp) == "employee 1 Jane Jane"
    assert str(emp) == "Jane Smith []"


def test_employee_as_dict():
    emp = Employee("Alice", "Johnson")
    emp.id = 10

    skill1 = ESkill("Python")
    skill1.id = 1
    skill2 = ESkill("Java")
    skill2.id = 2

    emp.skills = [skill1, skill2]
    dep = Department(department_name="dep")
    dep.id = 1

    emp.department = dep

    # when
    emp_as_dict = emp.as_dict()

    if emp_as_dict["department"]:
        emp_as_dict["department"] = {
            "id": emp_as_dict["department"].id,
            "name": emp_as_dict["department"].name,
        }

    assert isinstance(emp_as_dict, dict)
    assert emp_as_dict["id"] == 10
    assert emp_as_dict["first_name"] == "Alice"
    assert emp_as_dict["last_name"] == "Johnson"
    assert isinstance(emp_as_dict["department"], dict)
    assert emp_as_dict["department"]["id"] == 1
    assert emp_as_dict["department"]["name"] == "dep"
    assert isinstance(emp_as_dict["skills"], list)
    assert len(emp_as_dict["skills"]) == 2
    for skill_dict in emp_as_dict["skills"]:
        assert isinstance(skill_dict, dict)
        assert "id" in skill_dict
        assert "name" in skill_dict
