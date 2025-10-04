
from unittest import mock

import pytest

from models.employee import ESkill
from models.schemas import SkillSchema
from repositories.skills_repository import SkillRepository


def test_save_ok(test_db):
    # given
    session = test_db()
    repo = SkillRepository(session)
    s = ESkill(skill_name='testing skill')
    # when
    result = repo.add(s)
    assert result.id > 0
    assert s.id == result.id


def test_as_dict_ok():
    # given
    s = ESkill('test skill')
    # when
    s_as_dict = s.as_dict()
    # then
    assert isinstance(s_as_dict, dict)


# def test_as_dict_fail():
#     # when
#     with pytest.raises(TypeError) as exc:
#         s = ESkill()
#     # then
#     assert exc is not None


def test_update_ok(test_db, setup_skill):
    # given
    repo, skill = setup_skill
    skill_schema = SkillSchema(name='test skill')
    # when
    repo.update(skill, skill_schema)
    # then
    updated = repo.get_by_id(skill.id)
    assert updated.name == skill_schema.name


def test_delete_ok(test_db, setup_skill):
    # given
    repo, skill = setup_skill
    skill_id = skill.id
    # when
    repo.delete(skill)
    # then
    found = repo.get_by_id(skill_id)
    assert found is None
