import { useEffect, useState } from 'react'
import axiosClient from '../../api/axiosClient.js'
import Loader from '../common/Loader.jsx'
import { format } from 'date-fns'

export default function AuditLogTable() {
  const [logs, setLogs] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    axiosClient.get('/audit-logs').then(({ data }) => {
      setLogs(data.items)
      setIsLoading(false)
    })
  }, [])

  if (isLoading) return <Loader label="Loading audit trail..." />

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="text-left text-slate-500">
          <th className="pb-2">Action</th>
          <th className="pb-2">Actor Role</th>
          <th className="pb-2">Resource</th>
          <th className="pb-2">Time</th>
        </tr>
      </thead>
      <tbody>
        {logs.map((log) => (
          <tr key={log.id} className="border-t border-slate-100">
            <td className="py-2 font-mono text-xs">{log.action}</td>
            <td className="py-2 capitalize">{log.actor_role}</td>
            <td className="py-2">{log.resource_type} {log.resource_id?.slice(-6)}</td>
            <td className="py-2 text-xs text-slate-400">{format(new Date(log.created_at), 'PPpp')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
