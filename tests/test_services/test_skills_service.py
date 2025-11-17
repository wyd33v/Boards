from models.employee import ESkill
from models.schemas import SkillSchema


def test_get_all_skills(skills_service, mock_repo):
    fake_skills = [ESkill(skill_name="Python"), ESkill(skill_name="Java")]
    mock_repo["skills"].get_all.return_value = fake_skills

    result = skills_service.get_all_skills()

    assert len(result) == 2
    assert result[0].name == "Python"
    assert result[1].name == "Java"
    mock_repo["skills"].get_all.assert_called_once()


def test_get_skill_found(skills_service, mock_repo):
    skill = ESkill(skill_name="Python")
    mock_repo["skills"].get_by_id.return_value = skill

    result = skills_service.get_skill(1)

    assert result.name == "Python"
    mock_repo["skills"].get_by_id.assert_called_once_with(1)


def test_get_skill_not_found(skills_service, mock_repo):
    mock_repo["skills"].get_by_id.return_value = None

    result = skills_service.get_skill(999)

    assert result is None
    mock_repo["skills"].get_by_id.assert_called_once_with(999)


def test_create_skill(skills_service, mock_repo):
    schema = SkillSchema(name="Go")
    saved_skill = ESkill(skill_name="Go")
    mock_repo["skills"].save.return_value = saved_skill

    result = skills_service.create_skill(schema)

    assert result.name == "Go"
    mock_repo["skills"].save.assert_called_once()


def test_update_skill_found(skills_service, mock_repo):
    existing = ESkill(skill_name="OldSkill")
    schema = SkillSchema(name="NewSkill")
    mock_repo["skills"].get_by_id.return_value = existing
    mock_repo["skills"].save.return_value = existing

    result = skills_service.update_skill(1, schema)

    assert result.name == "NewSkill"
    mock_repo["skills"].get_by_id.assert_called_once_with(1)
    mock_repo["skills"].save.assert_called_once_with(existing)


def test_update_skill_not_found(skills_service, mock_repo):
    schema = SkillSchema(name="Nonexistent")
    mock_repo["skills"].get_by_id.return_value = None

    result = skills_service.update_skill(999, schema)

    assert result is None
    mock_repo["skills"].get_by_id.assert_called_once_with(999)
    mock_repo["skills"].save.assert_not_called()


def test_delete_skill_found(skills_service, mock_repo):
    existing = ESkill(skill_name="DeleteMe")
    mock_repo["skills"].get_by_id.return_value = existing

    result = skills_service.delete_skill(1)

    assert result == {"ok": True}
    mock_repo["skills"].get_by_id.assert_called_once_with(1)
    mock_repo["skills"].delete.assert_called_once_with(existing)


def test_delete_skill_not_found(skills_service, mock_repo):
    mock_repo["skills"].get_by_id.return_value = None

    result = skills_service.delete_skill(999)

    assert result is None
    mock_repo["skills"].get_by_id.assert_called_once_with(999)
    mock_repo["skills"].delete.assert_not_called()
