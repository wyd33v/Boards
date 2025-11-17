from unittest.mock import ANY

from fastapi import status

from models.employee import Employee, ESkill

# ---------------------------------------------------------
# GET /skills/
# ---------------------------------------------------------


def test_get_skills_ok(test_client, mock_skill_service):
    skill1 = ESkill("Python")
    skill2 = ESkill("Java")
    skill1.id = 1
    skill2.id = 2
    mock_skill_service.get_all_skills.return_value = [skill1, skill2]

    response = test_client.get("/skills/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Python"
    mock_skill_service.get_all_skills.assert_called_once()


# ---------------------------------------------------------
# GET /skills/{pk}
# ---------------------------------------------------------
def test_get_skill_ok(test_client, mock_skill_service):
    skill = ESkill("Python")
    skill.id = 1
    mock_skill_service.get_skill.return_value = skill

    response = test_client.get("/skills/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Python"
    mock_skill_service.get_skill.assert_called_once_with(1)


def test_get_skill_not_found(test_client, mock_skill_service):
    mock_skill_service.get_skill.return_value = None

    response = test_client.get("/skills/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Skill not found"
    mock_skill_service.get_skill.assert_called_once_with(999)


# ---------------------------------------------------------
# POST /skills/
# ---------------------------------------------------------
def test_create_skill_ok(test_client, mock_skill_service):
    skill_schema = {"name": "Go"}
    skill = ESkill("Go")
    skill.id = 1
    mock_skill_service.create_skill.return_value = skill

    response = test_client.post("/skills/", json=skill_schema)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Go"
    mock_skill_service.create_skill.assert_called_once_with(ANY)


# ---------------------------------------------------------
# PUT /skills/{pk}
# ---------------------------------------------------------
def test_update_skill_ok(test_client, mock_skill_service):
    skill_schema = {"name": "UpdatedSkill"}
    skill = ESkill("UpdatedSkill")
    skill.id = 1
    mock_skill_service.update_skill.return_value = skill

    response = test_client.put("/skills/1", json=skill_schema)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "UpdatedSkill"
    mock_skill_service.update_skill.assert_called_once_with(1, ANY)


def test_update_skill_not_found(test_client, mock_skill_service):
    mock_skill_service.update_skill.return_value = None

    response = test_client.put("/skills/99", json={"name": "X"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Skill not found"
    mock_skill_service.update_skill.assert_called_once_with(99, ANY)


# ---------------------------------------------------------
# DELETE /skills/{pk}
# ---------------------------------------------------------
def test_delete_skill_ok(test_client, mock_skill_service):
    mock_skill_service.delete_skill.return_value = True

    response = test_client.delete("/skills/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
    mock_skill_service.delete_skill.assert_called_once_with(1)


def test_delete_skill_not_found(test_client, mock_skill_service):
    mock_skill_service.delete_skill.return_value = False

    response = test_client.delete("/skills/123")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Skill not found"
    mock_skill_service.delete_skill.assert_called_once_with(123)


# ---------------------------------------------------------
# GET /skills/{pk}/employees
# ---------------------------------------------------------
def test_get_all_employees_by_skill_ok(test_client, mock_skill_service):
    skill = ESkill("Python")
    skill.id = 1
    emp1 = Employee(fname="John", lname="Doe")
    emp1.id = 1
    emp2 = Employee(fname="Jane", lname="Smith")
    emp2.id = 2
    skill.employees = [emp1, emp2]
    mock_skill_service.get_skill.return_value = skill

    response = test_client.get("/skills/1/employees")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    mock_skill_service.get_skill.assert_called_once_with(1)


def test_get_all_employees_by_skill_not_found(test_client, mock_skill_service):
    mock_skill_service.get_skill.return_value = None

    response = test_client.get("/skills/999/employees")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Skill not found"
    mock_skill_service.get_skill.assert_called_once_with(999)


# ---------------------------------------------------------
# POST /skills/{pk}/employees/{employee_pk}
# ---------------------------------------------------------
def test_skill_add_employee_ok(test_client, mock_skill_service, mock_employee_service):
    skill = ESkill("Python")
    skill.id = 1
    emp = Employee(fname="John", lname="Doe")
    emp.id = 2
    skill.employees = []
    mock_skill_service.get_skill.return_value = skill
    mock_employee_service.get_employee.return_value = emp
    mock_skill_service.add_employee_to_skill.return_value = skill

    response = test_client.post("/skills/1/employees/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "John"
    mock_skill_service.get_skill.assert_called_once_with(1)
    mock_employee_service.get_employee.assert_called_once_with(2)
    mock_skill_service.add_employee_to_skill.assert_called_once_with(skill, emp)


def test_skill_add_employee_already_has_skill(
    test_client, mock_skill_service, mock_employee_service
):
    skill = ESkill("Python")
    skill.id = 1
    emp = Employee(fname="John", lname="Doe")
    emp.id = 2
    skill.employees = [emp]
    mock_skill_service.get_skill.return_value = skill
    mock_employee_service.get_employee.return_value = emp

    response = test_client.post("/skills/1/employees/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "John"
    # add_employee_to_skill should NOT be called because employee already has skill
    mock_skill_service.add_employee_to_skill.assert_not_called()


# ---------------------------------------------------------
# DELETE /skills/{pk}/employee/{employee_pk}
# ---------------------------------------------------------
def test_skill_delete_employee_ok(
    test_client, mock_skill_service, mock_employee_service
):
    skill = ESkill("Python")
    skill.id = 1
    emp = Employee(fname="John", lname="Doe")
    emp.id = 2
    skill.employees = [emp]
    mock_skill_service.get_skill.return_value = skill
    mock_employee_service.get_employee.return_value = emp
    mock_skill_service.remove_employee_from_skill.return_value = skill

    response = test_client.delete("/skills/1/employee/2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "John"
    mock_skill_service.remove_employee_from_skill.assert_called_once_with(skill, emp)
