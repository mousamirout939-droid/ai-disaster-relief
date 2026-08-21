import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import CapacityMeter from '../shelters/CapacityMeter.jsx'

const icon = L.divIcon({
  className: 'shelter-marker',
  html: `<div style="background:#1d4ed8;width:18px;height:18px;border-radius:4px;border:2px solid white;display:flex;align-items:center;justify-content:center;color:white;font-size:11px;">🏠</div>`,
  iconSize: [18, 18],
})

export default function ShelterMarker({ shelter }) {
  const [lng, lat] = shelter.location.coordinates
  return (
    <Marker position={[lat, lng]} icon={icon}>
      <Popup>
        <div className="space-y-2 min-w-[180px]">
          <p className="font-semibold">{shelter.name}</p>
          <p className="text-xs text-slate-500">{shelter.address_text}</p>
          <CapacityMeter occupied={shelter.capacity_occupied} total={shelter.capacity_total} />
        </div>
      </Popup>
    </Marker>
  )
}
