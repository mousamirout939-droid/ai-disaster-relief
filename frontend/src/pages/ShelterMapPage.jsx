import { useEffect } from 'react'
import MapView from '../components/map/MapView.jsx'
import ShelterList from '../components/shelters/ShelterList.jsx'
import { useShelterStore } from '../store/useShelterStore.js'
import { useGeolocation } from '../hooks/useGeolocation.js'

export default function ShelterMapPage() {
  const { location } = useGeolocation()
  const { shelters, fetchNearby, isLoading, selectShelter } = useShelterStore()

  useEffect(() => {
    if (location) fetchNearby(location.lng, location.lat)
  }, [location, fetchNearby])

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
      <div className="lg:col-span-2 h-[60vh]">
        <MapView shelters={shelters} incidents={[]} />
      </div>
      <div className="max-h-[60vh] overflow-y-auto">
        <ShelterList shelters={shelters} isLoading={isLoading} onSelect={selectShelter} />
      </div>
    </div>
  )
}
