import { Link } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth.js'
import Button from '../common/Button.jsx'

export default function Navbar() {
  const { user, logout } = useAuth()
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
      <Link to="/dashboard" className="text-lg font-bold text-emergency-critical">
        🆘 Disaster Relief Platform
      </Link>
      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-500">{user?.full_name} · {user?.role}</span>
        <Button variant="ghost" onClick={logout}>Log out</Button>
      </div>
    </header>
  )
}
