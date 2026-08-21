import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-3xl font-bold">404 — Page Not Found</h1>
      <Link to="/" className="text-brand-700 hover:underline">Return home</Link>
    </div>
  )
}
