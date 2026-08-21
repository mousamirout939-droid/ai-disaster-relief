import { Link } from 'react-router-dom'
import Button from '../components/common/Button.jsx'

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-900 px-6 text-center text-white">
      <h1 className="mb-4 text-4xl font-bold">🆘 AI Disaster Relief & Rescue Platform</h1>
      <p className="mb-8 max-w-xl text-slate-300">
        Report disasters in real time, find nearby shelters and food distribution centers, and get
        AI-guided emergency assistance — all in one platform built for resilience.
      </p>
      <div className="flex gap-4">
        <Link to="/login"><Button variant="primary">Log In</Button></Link>
        <Link to="/register"><Button variant="outline" className="text-white border-white hover:bg-white/10">Register</Button></Link>
      </div>
    </div>
  )
}
