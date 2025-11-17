from data.repository import Repository
from models.department import Department
from models.employee import Employee, ESkill


def test_department_crud(test_db):
    repo = Repository(Department, test_db)

    dep = Department("test1")
    saved = repo.save(dep)

    assert saved.id is not None
    assert saved.name == "test1"

    found = repo.get_by_id(saved.id)
    assert found.name == "test1"

    found_by_param = repo.get_by_param(name="test1")
    assert found_by_param.id == saved.id

    all_deps = repo.get_all()
    assert len(all_deps) == 1

    repo.delete(saved)
    assert repo.get_all() == []


def test_employee_crud(test_db):
    repo = Repository(Employee, test_db)

    emp = Employee("emp1", "forename")
    saved = repo.save(emp)

    assert saved.id is not None
    assert saved.first_name == "emp1"
    assert saved.last_name == "forename"

    found = repo.get_by_id(saved.id)
    assert found.first_name == "emp1"
    assert found.last_name == "forename"

    found_by_param = repo.get_by_param(first_name="emp1", last_name="forename")
    assert found_by_param.id == saved.id

    all_emps = repo.get_all()
    assert len(all_emps) == 1

    repo.delete(saved)
    assert repo.get_all() == []


def test_eskill_crud(test_db):
    repo = Repository(ESkill, test_db)

    skill = ESkill("skille")
    saved = repo.save(skill)

    assert saved.id is not None
    assert saved.name == "skille"

    found = repo.get_by_id(saved.id)
    assert found.name == "skille"

    found_by_param = repo.get_by_param(name="skille")
    assert found_by_param.id == saved.id

    all_skills = repo.get_all()
    assert len(all_skills) == 1

    repo.delete(saved)
    assert repo.get_all() == []
