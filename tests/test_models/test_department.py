
from unittest import mock

import pytest

from models.department import Department
from models.schemas import DepartmentSchema
from repositories.department_repository import DepartmentRepository


def test_as_dict_ok():
    # given
    d = Department(department_name="test_department")
    # when
    d_as_dict = d.as_dict()
    # then
    assert isinstance(d_as_dict, dict)
    assert "name" in d_as_dict


# def test_as_dict_fail():
#     # when
#     with pytest.raises(TypeError) as exc:
#         d = Department()
#     # then
#     assert exc is not None


def test_save_ok(test_db):
    # given
    session = test_db()
    repo = DepartmentRepository(session)
    d = Department(department_name="test_department")
    # when
    result = repo.add(d)
    # then
    assert result.id > 0
    assert d.id == result.id


def test_update_ok(test_db):
    # given
    session = test_db()
    repo = DepartmentRepository(session)
    d = Department(department_name='testname')
    repo.add(d)
    d_schema = DepartmentSchema(name='updated')
    # when
    repo.update(d, d_schema)
    # then
    updated = repo.get_by_id(d.id)
    assert updated.name == d_schema.name


def test_delete_ok(test_db):
    # given
    session = test_db()
    repo = DepartmentRepository(session)
    d = Department(department_name='testname')
    repo.add(d)
    dep_id = d.id
    # when
    repo.delete(d)
    # then
    found = repo.get_by_id(dep_id)
    assert found is None
