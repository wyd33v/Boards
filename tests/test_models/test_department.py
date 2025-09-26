
from unittest import mock

import pytest

from models.department import Department
from models.schemas import DepartmentSchema


def test_as_dict_ok():
    # given
    d = Department(department_name="test_department")
    # when
    d_as_dict = d.as_dict()
    # then
    assert isinstance(d_as_dict, dict)


def test_as_dict_fail():
    # when
    with pytest.raises(TypeError) as exc:
        d = Department(name="test_department",)
    # then
    assert exc is not None


def test_save_ok(test_db):
    # given
    d = Department(department_name="test_department")
    # when
    result = d.save()
    assert result > 0
    assert d.id > 0


def test_update_ok(test_db):
    # given
    d = Department(department_name='testing name')
    d_schema = DepartmentSchema(name='updated department name test')
    # when
    prev_id = d.save()
    d.update(d_schema)
    # then
    assert d.id == prev_id
    assert d.name == d_schema.name


def test_delete_ok(test_db):
    # given
    d = Department(department_name='testing name')
    # when
    prev_id = d.save()
    # then
    d.delete()
    find_id = Department.get_by_id(prev_id)
    assert find_id is None
