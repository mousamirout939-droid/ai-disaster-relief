import { Outlet } from 'react-router-dom'
import Navbar from './Navbar.jsx'
import Sidebar from './Sidebar.jsx'
import Footer from './Footer.jsx'
import AlertBanner from '../alerts/AlertBanner.jsx'

export default function DashboardLayout() {
  return (
    <div className="flex h-screen flex-col">
      <Navbar />
      <AlertBanner />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-slate-50 p-6">
          <Outlet />
        </main>
      </div>
      <Footer />
    </div>
  )
}
