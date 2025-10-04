
from unittest import mock

import pytest

from models.employee import Employee, ESkill
from models.department import Department
from models.schemas import EmployeeSchema
from repositories.employee_repository import EmployeeRepository
from repositories.skills_repository import SkillRepository
from repositories.department_repository import DepartmentRepository

BASE_URL = "/employees/"

payload = {"first_name": "test fname", "last_name": "test lname"}


def test_save_ok(test_db):
    # given
    session = test_db()
    repo = EmployeeRepository(session)
    e = Employee(fname='testname', lname='testlast')
    # when
    result = repo.add(e)
    # then
    assert result.id > 0
    assert e.id == result.id


def test_as_dict_ok():
    # given
    e = Employee(fname='testname', lname='testlast')
    # when
    e_as_dict = e.as_dict()
    # then
    assert isinstance(e_as_dict, dict)
    assert "first_name" in e_as_dict
    assert "last_name" in e_as_dict

# def test_as_dict_fail():
#     # when / then
#     with pytest.raises(TypeError):
#         e = Employee(fname='testname')  # missing lname


def test_update_ok(test_db, setup_employee):
    # given
    repo, employee = setup_employee
    e_schema = EmployeeSchema(first_name='updated', last_name='newname')
    # when
    repo.update(employee, e_schema)
    # then
    updated = repo.get_by_id(employee.id)
    assert updated.first_name == e_schema.first_name
    assert updated.last_name == e_schema.last_name


def test_delete_ok(setup_employee):
    # given
    repo, employee = setup_employee
    emp_id = employee.id
    # when
    repo.delete(employee)
    # then
    found = repo.get_by_id(emp_id)
    assert found is None


def test_add_skill(test_db):
    # given
    session = test_db()
    emp_repo = EmployeeRepository(session)
    skill_repo = SkillRepository(session)

    skill = skill_repo.add(ESkill(skill_name='testing skill'))
    employee = emp_repo.add(Employee(fname='testname', lname='testlast'))
    # when
    emp_repo.add_skill(employee, skill)
    # then
    reloaded = emp_repo.get_by_id(employee.id)
    assert len(reloaded.skills) == 1
    assert reloaded.skills[0].name == skill.name


def test_get_employees(test_client, setup_employee):
    # given
    # session = test_db()
    # repo = EmployeeRepository(session)
    # e = Employee(fname="testname", lname="testlast")
    # repo.add(e)

    repo, employee = setup_employee
    # when
    response = test_client.get(f"{BASE_URL}")
    # then
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["first_name"] == "test fname"
    assert data[0]["last_name"] == "test lname"


def test_get_employee_by_id(test_client, setup_employee):
    # given
    repo, employee = setup_employee
    # when
    response = test_client.get(f"{BASE_URL}{employee.id}")
    # then
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "test fname"
    assert data["last_name"] == "test lname"


def test_get_employee_not_found(test_client):
    # given
    # when
    response = test_client.get(f"{BASE_URL}{9999}")
    # then
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_employee(test_client):
    # given
    # when
    response = test_client.post(f"{BASE_URL}", json=payload)
    # then
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

    # ???
    get_resp = test_client.get(f"{BASE_URL}{data["id"]}")
    data = get_resp.json()
    assert data["first_name"] == "test fname"
    assert data["last_name"] == "test lname"


def test_update_employee(test_client, setup_employee):
    # given
    _, employee = setup_employee

    payload_update = {"first_name": "Updated", "last_name": "Name"}
    # when
    response = test_client.put(f"{BASE_URL}{employee.id}", json=payload_update)
    # then
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


def test_update_employee_not_found(test_client):
    # given
    # when
    response = test_client.put(f"{BASE_URL}{9999}", json=payload)
    # then
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_delete_employee(test_client, setup_employee):
    # given
    _, employee = setup_employee
    # when
    response = test_client.delete(f"{BASE_URL}{employee.id}")
    # then
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_delete_employee_not_found(test_client):
    # given
    # when
    response = test_client.delete(f"{BASE_URL}{9999}")
    # then
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_employee_add_skill(test_db, test_client):
    # given
    session = test_db()
    emp_repo = EmployeeRepository(session)
    skill_repo = SkillRepository(session)

    skill = skill_repo.add(ESkill(skill_name='testing skill'))
    employee = emp_repo.add(Employee(fname='testname', lname='testlast'))
    # when
    response = test_client.post(f"{BASE_URL}{employee.id}/skill/{skill.id}")
    # then
    assert response.status_code == 200
    data = response.json()
    assert any(s["name"] == "testing skill" for s in data["skills"])


def test_employee_delete_skill(test_db, test_client):
    # given
    session = test_db()
    emp_repo = EmployeeRepository(session)
    skill_repo = SkillRepository(session)

    skill = skill_repo.add(ESkill(skill_name='testing skill'))
    employee = emp_repo.add(Employee(fname='testname', lname='testlast'))
    emp_repo.add_skill(employee, skill)
    # when
    response = test_client.delete(f"{BASE_URL}{employee.id}/skill/{skill.id}")
    # then
    assert response.status_code == 200
    data = response.json()
    assert len(data["skills"]) == 0


def test_employee_add_department(test_db, test_client):
    # given
    session = test_db()
    emp_repo = EmployeeRepository(session)
    department_repo = DepartmentRepository(session)

    department = department_repo.add(Department(department_name='ramp'))
    employee = emp_repo.add(Employee(fname='testname', lname='testlast'))
    # when
    response = test_client.post(
        f"{BASE_URL}{employee.id}/department/{department.id}")
    # then
    assert response.status_code == 200
    data = response.json()
    assert data["department"]["name"] == "ramp"


def test_employee_delete_department(test_db, test_client):
    # given
    session = test_db()
    emp_repo = EmployeeRepository(session)
    department_repo = DepartmentRepository(session)

    department = department_repo.add(Department(department_name='ramp'))
    employee = emp_repo.add(Employee(fname='testname', lname='testlast'))

    emp_repo.set_department(employee, department)
    # when
    response = test_client.delete(
        f"{BASE_URL}{employee.id}/department")
    # then
    assert response.status_code == 200
    data = response.json()
    assert data["department"] is None
