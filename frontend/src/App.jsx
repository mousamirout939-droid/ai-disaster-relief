import { Routes, Route } from 'react-router-dom'
import DashboardLayout from './components/layout/DashboardLayout.jsx'
import ProtectedRoute from './components/common/ProtectedRoute.jsx'
import RoleGate from './components/common/RoleGate.jsx'
import LandingPage from './pages/LandingPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import CitizenDashboard from './pages/CitizenDashboard.jsx'
import VolunteerDashboard from './pages/VolunteerDashboard.jsx'
import AdminDashboard from './pages/AdminDashboard.jsx'
import ReportIncidentPage from './pages/ReportIncidentPage.jsx'
import ShelterMapPage from './pages/ShelterMapPage.jsx'
import ChatAssistantPage from './pages/ChatAssistantPage.jsx'
import NotFoundPage from './pages/NotFoundPage.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<CitizenDashboard />} />
          <Route path="/report-incident" element={<ReportIncidentPage />} />
          <Route path="/shelters" element={<ShelterMapPage />} />
          <Route path="/chat" element={<ChatAssistantPage />} />

          <Route element={<RoleGate allow={['volunteer', 'admin']} />}>
            <Route path="/volunteer" element={<VolunteerDashboard />} />
          </Route>

          <Route element={<RoleGate allow={['admin']} />}>
            <Route path="/admin" element={<AdminDashboard />} />
          </Route>
        </Route>
      </Route>

      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
