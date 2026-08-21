import { useState } from 'react'
import clsx from 'clsx'
import AnalyticsDashboard from '../components/admin/AnalyticsDashboard.jsx'
import UserManagementTable from '../components/admin/UserManagementTable.jsx'
import AuditLogTable from '../components/admin/AuditLogTable.jsx'
import BroadcastForm from '../components/alerts/BroadcastForm.jsx'

const TABS = ['Analytics', 'Users', 'Audit Log', 'Broadcast Alert']

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('Analytics')

  return (
    <div>
      <h1 className="mb-4 text-xl font-bold">Admin Console</h1>
      <div className="mb-6 flex gap-2 border-b border-slate-200">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={clsx(
              'px-4 py-2 text-sm font-medium border-b-2',
              activeTab === tab ? 'border-brand-700 text-brand-700' : 'border-transparent text-slate-500',
            )}
          >
            {tab}
          </button>
        ))}
      </div>
      {activeTab === 'Analytics' && <AnalyticsDashboard />}
      {activeTab === 'Users' && <div className="card"><UserManagementTable /></div>}
      {activeTab === 'Audit Log' && <div className="card"><AuditLogTable /></div>}
      {activeTab === 'Broadcast Alert' && <BroadcastForm />}
    </div>
  )
}
