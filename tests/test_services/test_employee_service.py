from models.department import Department
from models.employee import Employee, ESkill
from models.schemas import EmployeeSchema


def test_get_all_employees(employee_service, mock_repo):
    fake_employees = [
        Employee(fname="name1", lname="sur1"),
        Employee(fname="name2", lname="sur2"),
    ]
    mock_repo["employee"].get_all.return_value = fake_employees

    result = employee_service.get_all_employees()

    assert len(result) == 2
    assert result[0].first_name == "name1"
    assert result[1].last_name == "sur2"
    mock_repo["employee"].get_all.assert_called_once()


def test_get_employee_found(employee_service, mock_repo):
    mock_repo["employee"].get_by_id.return_value = Employee(fname="name1", lname="sur1")

    result = employee_service.get_employee(1)

    assert result.first_name == "name1"
    mock_repo["employee"].get_by_id.assert_called_once_with(1)


def test_get_employee_not_found(employee_service, mock_repo):
    mock_repo["employee"].get_by_id.return_value = None

    result = employee_service.get_employee(999)

    assert result is None
    mock_repo["employee"].get_by_id.assert_called_once_with(999)


def test_create_employee(employee_service, mock_repo):
    schema = EmployeeSchema(first_name="name1", last_name="name2")
    saved_employee = Employee(fname="name1", lname="name2")
    mock_repo["employee"].save.return_value = saved_employee

    result = employee_service.create_employee(schema)

    assert result.first_name == "name1"
    assert result.last_name == "name2"
    mock_repo["employee"].save.assert_called_once()


def test_update_employee_found(employee_service, mock_repo):
    existing = Employee(fname="New", lname="Name")
    schema = EmployeeSchema(first_name="New", last_name="Name")
    mock_repo["employee"].get_by_id.return_value = existing
    mock_repo["employee"].save.return_value = existing

    result = employee_service.update_employee(1, schema)

    assert result.first_name == "New"
    assert result.last_name == "Name"
    mock_repo["employee"].get_by_id.assert_called_once_with(1)
    mock_repo["employee"].save.assert_called_once_with(existing)


def test_update_employee_not_found(employee_service, mock_repo):
    schema = EmployeeSchema(first_name="Nonexistent", last_name="User")
    mock_repo["employee"].get_by_id.return_value = None

    result = employee_service.update_employee(999, schema)

    assert result is None
    mock_repo["employee"].get_by_id.assert_called_once_with(999)
    mock_repo["employee"].save.assert_not_called()


def test_delete_employee_found(employee_service, mock_repo):
    existing = Employee(fname="Delete", lname="Me")
    mock_repo["employee"].get_by_id.return_value = existing

    result = employee_service.delete_employee(1)

    assert result == {"ok": True}
    mock_repo["employee"].get_by_id.assert_called_once_with(1)
    mock_repo["employee"].delete.assert_called_once_with(existing)


def test_delete_employee_not_found(employee_service, mock_repo):
    mock_repo["employee"].get_by_id.return_value = None

    result = employee_service.delete_employee(999)

    assert result is None
    mock_repo["employee"].get_by_id.assert_called_once_with(999)
    mock_repo["employee"].delete.assert_not_called()


def test_add_skill_to_employee(employee_service, mock_repo):
    employee = Employee(fname="John", lname="Doe")
    skill = ESkill(skill_name="skill1")

    result = employee_service.add_skill_to_employee(employee, skill)

    assert skill in result.skills
    mock_repo["employee"].save.assert_called_once_with(employee)


def test_remove_skill_from_employee(employee_service, mock_repo):
    skill = ESkill(skill_name="skill1")
    employee = Employee(fname="John", lname="Doe")
    employee.skills.append(skill)
    result = employee_service.remove_skill_from_employee(employee, skill)

    assert skill not in result.skills
    mock_repo["employee"].save.assert_called_once_with(employee)


def test_set_department_for_employee(employee_service, mock_repo):
    employee = Employee(fname="John", lname="Doe")
    dept = Department(department_name="IT")

    result = employee_service.set_department_for_employee(employee, dept)

    assert result.department == dept
    mock_repo["employee"].save.assert_called_once_with(employee)


def test_delete_department_from_employee(employee_service, mock_repo):
    dept = Department(department_name="IT")
    employee = Employee(fname="John", lname="Doe")
    employee.department = dept

    result = employee_service.delete_department_from_employee(employee)

    assert result.department is None
    mock_repo["employee"].save.assert_called_once_with(employee)
