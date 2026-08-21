"""
Role-Based Access Control enforcement.

Usage:
    @router.post("/incidents/{id}/verify")
    async def verify_incident(current_user=Depends(require_roles("volunteer", "admin"))):
        ...

RBAC matrix (summarized — see docs/RBAC_MATRIX.md for full detail):
  citizen    -> create incidents, view shelters/alerts, chat with AI, request aid
  volunteer  -> citizen perms + verify incidents, update shelter inventory
  admin      -> full CRUD on users/incidents/shelters, broadcast alerts, audit log access
"""
from collections.abc import Callable
from enum import StrEnum

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_active_user
from app.schemas.user import UserInDB


class Role(StrEnum):
    CITIZEN = "citizen"
    VOLUNTEER = "volunteer"
    ADMIN = "admin"


# Explicit role hierarchy: admin inherits volunteer & citizen permissions,
# volunteer inherits citizen permissions.
ROLE_HIERARCHY: dict[Role, set[Role]] = {
    Role.CITIZEN: {Role.CITIZEN},
    Role.VOLUNTEER: {Role.CITIZEN, Role.VOLUNTEER},
    Role.ADMIN: {Role.CITIZEN, Role.VOLUNTEER, Role.ADMIN},
}


def require_roles(*allowed_roles: str) -> Callable:
    """FastAPI dependency factory enforcing that current_user.role is permitted."""
    allowed: set[str] = {r.lower() for r in allowed_roles}

    async def _dependency(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
        user_role = Role(current_user.role)
        effective_roles = {r.value for r in ROLE_HIERARCHY.get(user_role, {user_role})}
        if not (effective_roles & allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {sorted(allowed)}. User role: {current_user.role}",
            )
        return current_user

    return _dependency


def require_self_or_roles(*allowed_roles: str) -> Callable:
    """Allow access if the caller owns the resource (matches path user_id) OR has an allowed role."""

    async def _dependency(
        user_id: str,
        current_user: UserInDB = Depends(get_current_active_user),
    ) -> UserInDB:
        if str(current_user.id) == user_id:
            return current_user
        allowed: set[str] = {r.lower() for r in allowed_roles}
        user_role = Role(current_user.role)
        effective_roles = {r.value for r in ROLE_HIERARCHY.get(user_role, {user_role})}
        if not (effective_roles & allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource.",
            )
        return current_user

    return _dependency
