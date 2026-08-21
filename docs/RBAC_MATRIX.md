# RBAC Matrix

Roles form a hierarchy: **admin** ⊃ **volunteer** ⊃ **citizen**. Higher roles inherit
all permissions of lower roles (`app/dependencies/rbac.py::ROLE_HIERARCHY`).

| Capability                                   | Citizen | Volunteer | Admin |
|-----------------------------------------------|:-------:|:---------:|:-----:|
| Register / log in                              | ✅      | ✅        | ✅    |
| Report a disaster incident (with image)        | ✅      | ✅        | ✅    |
| View shelters / food distribution centers      | ✅      | ✅        | ✅    |
| Chat with AI emergency assistant               | ✅      | ✅        | ✅    |
| Submit an aid request                          | ✅      | ✅        | ✅    |
| Verify / reject incident reports               | ❌      | ✅        | ✅    |
| Update shelter inventory (food/water/medical)  | ❌      | ✅        | ✅    |
| Coordinate local relief distribution           | ❌      | ✅        | ✅    |
| Create / edit / delete shelters                | ❌      | ❌ (edit only) | ✅ |
| Broadcast platform-wide emergency alerts       | ❌      | ❌        | ✅    |
| Manage users (suspend, change role)            | ❌      | ❌        | ✅    |
| View audit logs                                | ❌      | ❌        | ✅    |
| View analytics dashboard                       | ❌      | ❌        | ✅    |

## Enforcement
- `require_roles(*roles)` — FastAPI dependency, 403s if the caller's effective
  role set doesn't intersect the allowed set.
- `require_self_or_roles(*roles)` — allows a user to act on their own resource
  (e.g. update their own profile) OR requires an elevated role.
- All sensitive admin/volunteer actions are recorded via `AuditService.log(...)`
  into the `audit_logs` collection (180-day TTL).

## Volunteer onboarding
Volunteers self-register but are created with `volunteer_verified=False` and
cannot perform volunteer-gated actions until an admin sets `volunteer_verified=True`
via `PATCH /users/{id}/admin`. This prevents unverified accounts from claiming
volunteer privileges immediately after signup.
