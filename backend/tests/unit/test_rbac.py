import pytest
from fastapi import HTTPException

from app.dependencies.rbac import ROLE_HIERARCHY, Role


def test_admin_inherits_all_roles():
    assert ROLE_HIERARCHY[Role.ADMIN] == {Role.CITIZEN, Role.VOLUNTEER, Role.ADMIN}


def test_citizen_has_no_elevated_roles():
    assert ROLE_HIERARCHY[Role.CITIZEN] == {Role.CITIZEN}


def test_volunteer_inherits_citizen():
    assert Role.CITIZEN in ROLE_HIERARCHY[Role.VOLUNTEER]
