import { useEffect } from 'react'
import clsx from 'clsx'
import { useAlertStore } from '../../store/useAlertStore.js'
import { useWebSocket } from '../../hooks/useWebSocket.js'

const SEVERITY_STYLES = {
  info: 'bg-blue-50 text-blue-800 border-blue-200',
  warning: 'bg-amber-50 text-amber-800 border-amber-200',
  critical: 'bg-red-50 text-red-800 border-red-200',
}

export default function AlertBanner() {
  const { activeAlerts, pushRealtimeAlert, dismissAlert } = useAlertStore()

  useWebSocket((msg) => {
    if (msg.type === 'alert.broadcast') pushRealtimeAlert(msg)
  })

  if (!activeAlerts.length) return null

  return (
    <div className="space-y-1 px-4 py-2">
      {activeAlerts.slice(0, 3).map((alert) => (
        <div
          key={alert.id || alert.title}
          className={clsx('flex items-center justify-between rounded-lg border px-4 py-2 text-sm', SEVERITY_STYLES[alert.severity])}
        >
          <div>
            <span className="font-semibold">{alert.title}</span> — {alert.message}
          </div>
          <button onClick={() => dismissAlert(alert.id)} className="ml-4 text-xs opacity-60 hover:opacity-100">✕</button>
        </div>
      ))}
    </div>
  )
}
