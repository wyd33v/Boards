from unittest.mock import ANY

from fastapi import status

from models.department import Department


# ---------------------------------------------------------
# GET /
# ---------------------------------------------------------
def test_get_departments_ok(test_client, mock_department_service):
    dep1 = Department(department_name="HR")
    dep2 = Department(department_name="Finance")
    dep1.id = 1
    dep2.id = 2
    mock_department_service.get_all_departments.return_value = [dep1, dep2]

    response = test_client.get("/departments/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "HR"
    mock_department_service.get_all_departments.assert_called_once()


# ---------------------------------------------------------
# GET /{pk}
# ---------------------------------------------------------
def test_get_department_ok(test_client, mock_department_service):
    dep = Department(department_name="IT")
    dep.id = 1
    mock_department_service.get_department.return_value = dep

    response = test_client.get("/departments/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "IT"
    mock_department_service.get_department.assert_called_once_with(1)


def test_get_department_not_found(test_client, mock_department_service):
    mock_department_service.get_department.return_value = None

    response = test_client.get("/departments/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Department not found"
    mock_department_service.get_department.assert_called_once_with(999)


# ---------------------------------------------------------
# POST /
# ---------------------------------------------------------
def test_create_department_ok(test_client, mock_department_service):
    dep_schema = {"name": "New Department"}
    dep = Department(department_name="New Department")
    dep.id = 1
    mock_department_service.create_department.return_value = dep

    response = test_client.post("/departments/", json=dep_schema)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Department"
    mock_department_service.create_department.assert_called_once_with(ANY)


# ---------------------------------------------------------
# PUT /{pk}
# ---------------------------------------------------------
def test_update_department_ok(test_client, mock_department_service):
    dep_schema = {"name": "Updated Department"}
    dep = Department(department_name="Updated Department")
    dep.id = 1
    mock_department_service.update_department.return_value = dep

    response = test_client.put("/departments/1", json=dep_schema)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Department"
    mock_department_service.update_department.assert_called_once_with(1, ANY)


def test_update_department_not_found(test_client, mock_department_service):
    mock_department_service.update_department.return_value = None

    response = test_client.put("/departments/99", json={"name": "Whatever"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Department not found"
    mock_department_service.update_department.assert_called_once_with(99, ANY)


# ---------------------------------------------------------
# DELETE /{pk}
# ---------------------------------------------------------
def test_delete_department_ok(test_client, mock_department_service):
    mock_department_service.delete_department.return_value = True

    response = test_client.delete("/departments/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True
    mock_department_service.delete_department.assert_called_once_with(1)


def test_delete_department_not_found(test_client, mock_department_service):
    mock_department_service.delete_department.return_value = False

    response = test_client.delete("/departments/123")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Department not found"
    mock_department_service.delete_department.assert_called_once_with(123)
