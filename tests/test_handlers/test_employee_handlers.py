from unittest.mock import ANY

from fastapi import status

from models.department import Department
from models.employee import Employee, ESkill


def test_get_employees_ok(test_client, mock_employee_service):
    emp1 = Employee(fname="name1", lname="name2")
    emp2 = Employee(fname="name3", lname="name4")
    emp1.id = 1
    emp2.id = 2
    mock_employee_service.get_all_employees.return_value = [emp1, emp2]

    response = test_client.get("/employees/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["first_name"] == "name1"
    mock_employee_service.get_all_employees.assert_called_once()


# ---------------------------------------------------------
# GET /{pk}
# ---------------------------------------------------------
def test_get_employee_ok(test_client, mock_employee_service):
    emp = Employee(fname="John", lname="Doe")
    emp.id = 1
    mock_employee_service.get_employee.return_value = emp

    response = test_client.get("/employees/1")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["first_name"] == "John"
    mock_employee_service.get_employee.assert_called_once_with(1)


def test_get_employee_not_found(test_client, mock_employee_service):
    mock_employee_service.get_employee.return_value = None

    response = test_client.get("/employees/99")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Employee not found"


# ---------------------------------------------------------
# POST /
# ---------------------------------------------------------
def test_create_employee_ok(test_client, mock_employee_service):
    emp_schema = {"first_name": "Alice", "last_name": "Smith"}
    emp = Employee(fname="Alice", lname="Smith")
    emp.id = 10
    mock_employee_service.create_employee.return_value = emp

    response = test_client.post("/employees/", json=emp_schema)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Alice"
    mock_employee_service.create_employee.assert_called_once()


# ---------------------------------------------------------
# PUT /{pk}
# ---------------------------------------------------------
def test_update_employee_ok(test_client, mock_employee_service):
    emp_schema = {"first_name": "John", "last_name": "Doe"}
    emp = Employee(fname="John", lname="Doe")
    emp.id = 1
    mock_employee_service.update_employee.return_value = emp

    response = test_client.put("/employees/1", json=emp_schema)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "John"
    mock_employee_service.update_employee.assert_called_once_with(1, ANY)


def test_update_employee_not_found(test_client, mock_employee_service):
    mock_employee_service.update_employee.return_value = None

    response = test_client.put(
        "/employees/1", json={"first_name": "X", "last_name": "Y"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Employee not found"


# ---------------------------------------------------------
# DELETE /{pk}
# ---------------------------------------------------------
def test_delete_employee_ok(test_client, mock_employee_service):
    mock_employee_service.delete_employee.return_value = {"ok": True}

    response = test_client.delete("/employees/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ok": True}
    mock_employee_service.delete_employee.assert_called_once_with(1)


def test_delete_employee_not_found(test_client, mock_employee_service):
    mock_employee_service.delete_employee.return_value = None

    response = test_client.delete("/employees/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Employee not found"


# ---------------------------------------------------------
# POST /{pk}/skill/{skill_pk}
# ---------------------------------------------------------
def test_employee_add_skill_ok(test_client, mock_employee_service, mock_skill_service):
    emp = Employee(fname="John", lname="Doe")
    emp.id = 1
    skill = ESkill("Python")
    skill.id = 2

    mock_employee_service.get_employee.return_value = emp
    mock_skill_service.get_skill.return_value = skill
    mock_employee_service.add_skill_to_employee.return_value = emp

    response = test_client.post("/employees/1/skill/2")
    assert response.status_code == status.HTTP_200_OK
    mock_employee_service.add_skill_to_employee.assert_called_once_with(emp, skill)


def test_employee_add_skill_employee_not_found(
    test_client, mock_employee_service, mock_skill_service
):
    mock_employee_service.get_employee.return_value = None
    response = test_client.post("/employees/1/skill/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Employee not found"


def test_employee_add_skill_skill_not_found(
    test_client, mock_employee_service, mock_skill_service
):
    emp = Employee(fname="John", lname="Doe")
    mock_employee_service.get_employee.return_value = emp
    mock_skill_service.get_skill.return_value = None

    response = test_client.post("/employees/1/skill/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Skill not found"


# ---------------------------------------------------------
# DELETE /{pk}/skill/{skill_pk}
# ---------------------------------------------------------
def test_employee_remove_skill_ok(
    test_client, mock_employee_service, mock_skill_service
):
    emp = Employee(fname="John", lname="Doe")
    emp.id = 1
    skill = ESkill("Python")
    skill.id = 2
    mock_employee_service.get_employee.return_value = emp
    mock_skill_service.get_skill.return_value = skill
    mock_employee_service.remove_skill_from_employee.return_value = emp

    response = test_client.delete("/employees/1/skill/2")
    assert response.status_code == status.HTTP_200_OK
    mock_employee_service.remove_skill_from_employee.assert_called_once_with(emp, skill)


# ---------------------------------------------------------
# POST /{pk}/department/{department_pk}
# ---------------------------------------------------------
def test_employee_add_department_ok(
    test_client, mock_employee_service, mock_department_service
):
    emp = Employee(fname="John", lname="Doe")
    emp.id = 1
    dep = Department(department_name="IT")
    dep.id = 2

    mock_employee_service.get_employee.return_value = emp
    mock_department_service.get_department.return_value = dep
    mock_employee_service.set_department_for_employee.return_value = emp

    response = test_client.post("/employees/1/department/2")
    assert response.status_code == status.HTTP_200_OK
    mock_employee_service.set_department_for_employee.assert_called_once_with(emp, dep)


# ---------------------------------------------------------
# DELETE /{pk}/department
# ---------------------------------------------------------
def test_employee_delete_department_ok(test_client, mock_employee_service):
    emp = Employee(fname="John", lname="Doe")
    emp.id = 1
    mock_employee_service.get_employee.return_value = emp
    mock_employee_service.delete_department_from_employee.return_value = emp

    response = test_client.delete("/employees/1/department")
    assert response.status_code == status.HTTP_200_OK
    mock_employee_service.delete_department_from_employee.assert_called_once_with(emp)
