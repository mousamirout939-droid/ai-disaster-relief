import { useEffect, useRef, useState } from 'react'
import { useAuthStore } from '../store/useAuthStore.js'

export function useWebSocket(onMessage) {
  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef(null)
  const accessToken = useAuthStore((s) => s.accessToken)

  useEffect(() => {
    if (!accessToken) return undefined

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${protocol}://${window.location.host}/ws?token=${accessToken}`)
    wsRef.current = ws

    ws.onopen = () => setIsConnected(true)
    ws.onclose = () => setIsConnected(false)
    ws.onmessage = (event) => {
      try {
        onMessage?.(JSON.parse(event.data))
      } catch {
        // ignore malformed frames
      }
    }

    const heartbeat = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) ws.send('ping')
    }, 30000)

    return () => {
      clearInterval(heartbeat)
      ws.close()
    }
  }, [accessToken, onMessage])

  return { isConnected }
}
