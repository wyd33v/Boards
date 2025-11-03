# test_department_service.py
from models.department import Department
from models.schemas import DepartmentSchema


def test_get_all_departments(department_service, mock_repo):
    # given
    fake_departments = [Department(
        department_name="dep1"), Department(department_name="dep2")]
    mock_repo["department"].get_all.return_value = fake_departments

    # when
    result = department_service.get_all_departments()

    # then
    assert len(result) == 2
    assert result[0].name == "dep1"
    assert result[1].name == "dep2"
    mock_repo["department"].get_all.assert_called_once()


def test_get_department_found(department_service, mock_repo):
    # given
    mock_repo["department"].get_by_id.return_value = Department(department_name="IT")
    # when
    result = department_service.get_department(1)
    # then
    assert result.name == "IT"
    mock_repo["department"].get_by_id.assert_called_once_with(1)


def test_get_department_not_found(department_service, mock_repo):
    # given
    mock_repo["department"].get_by_id.return_value = None
    # when
    result = department_service.get_department(999)
    # then
    assert result is None
    mock_repo["department"].get_by_id.assert_called_once_with(999)


def test_create_department(department_service, mock_repo):
    # given
    schema = DepartmentSchema(name="Marketing")
    saved_department = Department(department_name="Marketing")
    mock_repo["department"].save.return_value = saved_department
    # when
    result = department_service.create_department(schema)
    # then
    assert result.name == "Marketing"
    mock_repo["department"].save.assert_called_once()


def test_update_department_found(department_service, mock_repo):
    # given
    existing = Department(department_name="Old Dept")
    schema = DepartmentSchema(name="Updated Dept")
    mock_repo["department"].get_by_id.return_value = existing
    mock_repo["department"].save.return_value = existing
    # when
    result = department_service.update_department(1, schema)
    # then
    assert result.name == "Updated Dept"
    mock_repo["department"].get_by_id.assert_called_once_with(1)
    mock_repo["department"].save.assert_called_once_with(existing)


def test_update_department_not_found(department_service, mock_repo):
    # given
    mock_repo["department"].get_by_id.return_value = None
    schema = DepartmentSchema(name="Nonexistent")
    # when
    result = department_service.update_department(999, schema)
    # then
    assert result is None
    mock_repo["department"].get_by_id.assert_called_once_with(999)
    mock_repo["department"].save.assert_not_called()


def test_delete_department_found(department_service, mock_repo):
    # given
    existing = Department(department_name="DeleteMe")
    mock_repo["department"].get_by_id.return_value = existing
    # when
    result = department_service.delete_department(1)
    # then
    assert result == {"ok": True}
    mock_repo["department"].get_by_id.assert_called_once_with(1)
    mock_repo["department"].delete.assert_called_once_with(existing)


def test_delete_department_not_found(department_service, mock_repo):
    # given
    mock_repo["department"].get_by_id.return_value = None
    # when
    result = department_service.delete_department(999)
    # then
    assert result is None
    mock_repo["department"].get_by_id.assert_called_once_with(999)
    mock_repo["department"].delete.assert_not_called()
