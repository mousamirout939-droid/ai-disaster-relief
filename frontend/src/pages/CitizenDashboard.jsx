import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import MapView from '../components/map/MapView.jsx'
import GeolocationControl from '../components/map/GeolocationControl.jsx'
import { useIncidentStore } from '../store/useIncidentStore.js'
import { useShelterStore } from '../store/useShelterStore.js'
import { useGeolocation } from '../hooks/useGeolocation.js'
import Button from '../components/common/Button.jsx'

export default function CitizenDashboard() {
  const { location } = useGeolocation()
  const { incidents, fetchNearby: fetchIncidents } = useIncidentStore()
  const { shelters, fetchNearby: fetchShelters } = useShelterStore()

  useEffect(() => {
    if (location) {
      fetchIncidents(location.lng, location.lat)
      fetchShelters(location.lng, location.lat)
    }
  }, [location, fetchIncidents, fetchShelters])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold">Situation Overview</h1>
        <Link to="/report-incident"><Button variant="danger">🚨 Report Emergency</Button></Link>
      </div>
      <div className="relative h-[65vh]">
        <MapView incidents={incidents} shelters={shelters} />
        <GeolocationControl />
      </div>
    </div>
  )
}
