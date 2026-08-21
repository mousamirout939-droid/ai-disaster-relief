import { useEffect, useState } from 'react'

export function useGeolocation(options = { enableHighAccuracy: true }) {
  const [location, setLocation] = useState(null)
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by this browser.')
      setIsLoading(false)
      return
    }
    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        setLocation({ lat: position.coords.latitude, lng: position.coords.longitude })
        setIsLoading(false)
      },
      (err) => {
        setError(err.message)
        setIsLoading(false)
      },
      options,
    )
    return () => navigator.geolocation.clearWatch(watchId)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return { location, error, isLoading }
}
