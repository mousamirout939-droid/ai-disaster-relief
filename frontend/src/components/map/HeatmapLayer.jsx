import { useEffect } from 'react'
import { useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet.heat'

/** Renders an incident-density heatmap layer, weighted by severity. */
const SEVERITY_WEIGHT = { low: 0.3, moderate: 0.5, high: 0.75, critical: 1.0 }

export default function HeatmapLayer({ incidents }) {
  const map = useMap()

  useEffect(() => {
    if (!incidents.length) return undefined
    const points = incidents.map((i) => {
      const [lng, lat] = i.location.coordinates
      return [lat, lng, SEVERITY_WEIGHT[i.severity] || 0.4]
    })
    const heatLayer = L.heatLayer(points, { radius: 25, blur: 20, maxZoom: 15 })
    heatLayer.addTo(map)
    return () => map.removeLayer(heatLayer)
  }, [incidents, map])

  return null
}
