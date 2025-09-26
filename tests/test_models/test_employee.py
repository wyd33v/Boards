
from unittest import mock

import pytest

from models.employee import Employee, ESkill
from models.schemas import EmployeeSchema


def test_save_ok(test_db):
    # given
    e = Employee(fname='testname', lname='testlast')
    # when
    result = e.save()
    assert result > 0
    assert e.id > 0


def test_as_dict_ok():
    # given
    e = Employee(fname='testname', lname='testlast')
    # when
    e_as_dict = e.as_dict()
    # then
    assert isinstance(e_as_dict, dict)


def test_as_dict_fail():
    # when
    with pytest.raises(TypeError) as exc:
        e = Employee(fname='testname',)
    # then
    assert exc is not None


def test_update_ok(test_db):
    # given
    e = Employee(fname='testname', lname='testlast')
    e_schema = EmployeeSchema(
        first_name='updated name test', last_name='testlast')
    # when
    prev_id = e.save()
    e.update(e_schema)
    # then
    assert e.id == prev_id
    assert e.first_name == e_schema.first_name
    assert e.last_name == e_schema.last_name


def test_delete_ok(test_db):
    # given
    e = Employee(fname='testname', lname='testlast')
    # when
    prev_id = e.save()
    # then
    e.delete()
    find_id = Employee.get_by_id(prev_id)
    assert find_id is None

# def test_add_skill(test_db):
#     # given
#     e = Employee(fname='testname', lname='testlast')
#     s = ESkill(skill_name='testing skill')
#     # when
#     prev_id = e.save()
#     s.save()
#     e.add_skill(s)
#     # then
#     assert 1==1
    # assert any(skill.skill_name == "testing skill" for skill in e.skills)
