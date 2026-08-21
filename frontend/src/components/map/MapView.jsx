import { MapContainer, TileLayer, useMap } from 'react-leaflet'
import { useEffect } from 'react'
import 'leaflet/dist/leaflet.css'
import IncidentMarker from './IncidentMarker.jsx'
import ShelterMarker from './ShelterMarker.jsx'
import HeatmapLayer from './HeatmapLayer.jsx'
import { useMapStore } from '../../store/useMapStore.js'

function RecenterOnChange({ center, zoom }) {
  const map = useMap()
  useEffect(() => {
    map.setView(center, zoom)
  }, [center, zoom, map])
  return null
}

export default function MapView({ incidents = [], shelters = [] }) {
  const { center, zoom, activeLayers } = useMapStore()

  return (
    <MapContainer center={center} zoom={zoom} className="h-full w-full rounded-xl" scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <RecenterOnChange center={center} zoom={zoom} />

      {activeLayers.incidents && incidents.map((incident) => (
        <IncidentMarker key={incident.id} incident={incident} />
      ))}

      {activeLayers.shelters && shelters.map((shelter) => (
        <ShelterMarker key={shelter.id} shelter={shelter} />
      ))}

      {activeLayers.heatmap && <HeatmapLayer incidents={incidents} />}
    </MapContainer>
  )
}
