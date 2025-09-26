
from unittest import mock

import pytest

from models.employee import ESkill
from models.schemas import SkillSchema


def test_save_ok(test_db):
    # given
    s = ESkill(skill_name='test skill')
    # when
    result = s.save()
    assert result > 0
    assert s.id > 0


def test_as_dict_ok():
    # given
    s = ESkill('test skill')
    # when
    s_as_dict = s.as_dict()
    # then
    assert isinstance(s_as_dict, dict)


def test_as_dict_fail():
    # when
    with pytest.raises(TypeError) as exc:
        s = ESkill()
    # then
    assert exc is not None


def test_update_ok(test_db):
    # given
    s = ESkill(skill_name='test skill')
    s_schema = SkillSchema(name='new test name')
    # when
    prev_id = s.save()
    s.update(s_schema)
    # then
    assert s.id == prev_id
    assert s.name == s_schema.name

def test_delete_ok(test_db):
    # given
    s = ESkill(skill_name = 'skill name')
    # when
    prev_id = s.save()
    # then
    s.delete()
    find_id = ESkill.get_by_id(prev_id)
    assert find_id is None
