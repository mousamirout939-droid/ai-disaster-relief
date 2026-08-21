import SeverityBadge from './SeverityBadge.jsx'

export default function IncidentCard({ incident, onVerify }) {
  return (
    <div className="card flex items-start justify-between gap-4">
      <div>
        <div className="mb-1 flex items-center gap-2">
          <h3 className="font-semibold capitalize">{incident.category.replace('_', ' ')}</h3>
          <SeverityBadge severity={incident.severity} />
        </div>
        <p className="text-sm text-slate-600">{incident.description}</p>
        <p className="mt-1 text-xs text-slate-400">Status: {incident.status.replace('_', ' ')}</p>
      </div>
      {onVerify && incident.status === 'pending_review' && (
        <div className="flex shrink-0 gap-2">
          <button onClick={() => onVerify(incident.id, true)} className="text-sm text-green-600 hover:underline">Verify</button>
          <button onClick={() => onVerify(incident.id, false)} className="text-sm text-red-600 hover:underline">Reject</button>
        </div>
      )}
    </div>
  )
}
