
from unittest import mock

import pytest

from models.department import Department


def test_as_dict_ok():
    # given
    d = Department(department_name= "test_department")
    # when
    d_as_dict = d.as_dict()
    # then
    assert isinstance(d_as_dict, dict)

def test_as_dict_fail():
    # given
    
    # when
    with pytest.raises(TypeError) as exc:
        d = Department(name= "test_department",)
    # then
    assert exc is not None


def test_save_ok(test_db):
    with mock.patch("models.department.db_session") as db_session:
        db_session.return_value = test_db
        # given
        d = Department(department_name= "test_department")
        # when
        result = d.save()
        # then
        db_session.add.assert_called_once()
        db_session.commit.assert_called_once()
