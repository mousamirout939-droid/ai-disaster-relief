import { useEffect, useState } from 'react'

/**
 * Tracks online/offline status and exposes a queue for actions (like
 * incident reports) attempted while offline, to be flushed once
 * connectivity returns. Pairs with the PWA service worker's cache-first
 * strategy for read paths (shelters/incidents nearby).
 */
export function useOfflineSync(flushCallback) {
  const [isOnline, setIsOnline] = useState(navigator.onLine)
  const [pendingActions, setPendingActions] = useState([])

  useEffect(() => {
    const goOnline = async () => {
      setIsOnline(true)
      if (pendingActions.length && flushCallback) {
        await flushCallback(pendingActions)
        setPendingActions([])
      }
    }
    const goOffline = () => setIsOnline(false)

    window.addEventListener('online', goOnline)
    window.addEventListener('offline', goOffline)
    return () => {
      window.removeEventListener('online', goOnline)
      window.removeEventListener('offline', goOffline)
    }
  }, [pendingActions, flushCallback])

  const queueAction = (action) => setPendingActions((prev) => [...prev, action])

  return { isOnline, queueAction, pendingCount: pendingActions.length }
}
