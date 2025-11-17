from models.department import Department


def test_department_initialization():
    # given
    dep = Department(department_name="IT")

    # then
    assert dep.name == "IT"
    assert dep.id is None
    assert dep.employees == []


def test_department_repr_and_str():
    # given
    dep = Department(department_name="HR")
    dep.id = 5

    # when
    repr_str = repr(dep)
    str_str = str(dep)

    # then
    assert "department 5 HR" in repr_str
    assert str_str == "HR"


def test_department_as_dict():
    # given
    dep = Department(department_name="Finance")
    dep.id = 10

    # when
    result = dep.as_dict()

    # then
    assert isinstance(result, dict)
    assert result == {"id": 10, "name": "Finance"}
    assert "id" in result
    assert "name" in result
