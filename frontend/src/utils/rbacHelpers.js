const ROLE_HIERARCHY = {
  citizen: ['citizen'],
  volunteer: ['citizen', 'volunteer'],
  admin: ['citizen', 'volunteer', 'admin'],
}

export function canAccess(userRole, requiredRoles) {
  const effective = ROLE_HIERARCHY[userRole] || [userRole]
  return requiredRoles.some((r) => effective.includes(r))
}
