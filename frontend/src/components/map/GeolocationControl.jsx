import { useGeolocation } from '../../hooks/useGeolocation.js'
import { useMapStore } from '../../store/useMapStore.js'
import Button from '../common/Button.jsx'

export default function GeolocationControl() {
  const { location } = useGeolocation()
  const setUserLocation = useMapStore((s) => s.setUserLocation)

  return (
    <Button
      variant="outline"
      onClick={() => location && setUserLocation(location)}
      disabled={!location}
      className="absolute bottom-4 right-4 z-[1000] bg-white shadow"
    >
      📍 My Location
    </Button>
  )
}
