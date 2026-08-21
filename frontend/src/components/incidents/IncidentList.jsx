import IncidentCard from './IncidentCard.jsx'
import Loader from '../common/Loader.jsx'

export default function IncidentList({ incidents, isLoading, onVerify }) {
  if (isLoading) return <Loader label="Loading incidents..." />
  if (!incidents.length) return <p className="text-sm text-slate-400">No incidents reported nearby.</p>
  return (
    <div className="space-y-3">
      {incidents.map((incident) => (
        <IncidentCard key={incident.id} incident={incident} onVerify={onVerify} />
      ))}
    </div>
  )
}
