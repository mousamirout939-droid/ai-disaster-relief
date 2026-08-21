import { NavLink } from 'react-router-dom'
import clsx from 'clsx'
import { useAuth } from '../../hooks/useAuth.js'

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', roles: ['citizen', 'volunteer', 'admin'] },
  { to: '/report-incident', label: 'Report Incident', roles: ['citizen', 'volunteer', 'admin'] },
  { to: '/shelters', label: 'Shelter Map', roles: ['citizen', 'volunteer', 'admin'] },
  { to: '/chat', label: 'AI Assistant', roles: ['citizen', 'volunteer', 'admin'] },
  { to: '/volunteer', label: 'Volunteer Tools', roles: ['volunteer', 'admin'] },
  { to: '/admin', label: 'Admin Console', roles: ['admin'] },
]

export default function Sidebar() {
  const { user } = useAuth()
  const visibleItems = NAV_ITEMS.filter((item) => item.roles.includes(user?.role))

  return (
    <aside className="w-60 shrink-0 border-r border-slate-200 bg-white p-4">
      <nav className="flex flex-col gap-1">
        {visibleItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              clsx(
                'rounded-lg px-3 py-2 text-sm font-medium',
                isActive ? 'bg-brand-50 text-brand-700' : 'text-slate-600 hover:bg-slate-50',
              )
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
