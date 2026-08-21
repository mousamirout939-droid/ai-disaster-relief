import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import SeverityBadge from '../incidents/SeverityBadge.jsx'

const SEVERITY_COLORS = { low: '#65a30d', moderate: '#d97706', high: '#ea580c', critical: '#dc2626' }

function buildIcon(severity) {
  const color = SEVERITY_COLORS[severity] || '#64748b'
  return L.divIcon({
    className: 'incident-marker',
    html: `<div style="background:${color};width:16px;height:16px;border-radius:50%;border:2px solid white;box-shadow:0 0 4px rgba(0,0,0,0.4);"></div>`,
    iconSize: [16, 16],
  })
}

export default function IncidentMarker({ incident }) {
  const [lng, lat] = incident.location.coordinates
  return (
    <Marker position={[lat, lng]} icon={buildIcon(incident.severity)}>
      <Popup>
        <div className="space-y-1">
          <p className="font-semibold capitalize">{incident.category.replace('_', ' ')}</p>
          <SeverityBadge severity={incident.severity} />
          <p className="text-sm text-slate-600">{incident.description}</p>
        </div>
      </Popup>
    </Marker>
  )
}
