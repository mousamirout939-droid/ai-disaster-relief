import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { analyticsApi } from '../../api/analyticsApi.js'
import Loader from '../common/Loader.jsx'

const COLORS = ['#65a30d', '#d97706', '#ea580c', '#dc2626']

export default function AnalyticsDashboard() {
  const [data, setData] = useState(null)

  useEffect(() => {
    analyticsApi.getDashboard().then(({ data }) => setData(data))
  }, [])

  if (!data) return <Loader label="Loading analytics..." />

  const severityData = Object.entries(data.severity_breakdown).map(([name, value]) => ({ name, value }))
  const trendData = data.incidents_over_time.map((d) => ({ date: d._id, count: d.count }))

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <div className="card">
        <h3 className="mb-4 font-semibold">Incidents by Severity</h3>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={severityData} dataKey="value" nameKey="name" outerRadius={90} label>
              {severityData.map((_, idx) => <Cell key={idx} fill={COLORS[idx % COLORS.length]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="card">
        <h3 className="mb-4 font-semibold">Incident Trend</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={trendData}>
            <XAxis dataKey="date" tick={{ fontSize: 10 }} />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" fill="#1d4ed8" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="card lg:col-span-2">
        <h3 className="mb-2 font-semibold">Shelter Capacity Overview</h3>
        <p className="text-sm text-slate-600">
          {data.shelter_capacity.total_occupied} / {data.shelter_capacity.total_capacity} occupied across{' '}
          {data.shelter_capacity.shelter_count} shelters
        </p>
      </div>
    </div>
  )
}
