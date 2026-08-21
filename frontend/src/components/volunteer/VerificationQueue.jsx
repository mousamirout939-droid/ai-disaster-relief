import { useEffect } from 'react'
import IncidentList from '../incidents/IncidentList.jsx'
import { useIncidentStore } from '../../store/useIncidentStore.js'
import axiosClient from '../../api/axiosClient.js'
import { notify } from '../common/Toast.jsx'
import { useState } from 'react'

export default function VerificationQueue() {
  const [incidents, setIncidents] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const verifyIncident = useIncidentStore((s) => s.verifyIncident)

  const load = () => {
    setIsLoading(true)
    axiosClient.get('/incidents', { params: { status_filter: 'pending_review' } }).then(({ data }) => {
      setIncidents(data.items)
      setIsLoading(false)
    })
  }

  useEffect(load, [])

  const handleVerify = async (incidentId, approve) => {
    try {
      await verifyIncident(incidentId, approve)
      notify.success(approve ? 'Incident verified.' : 'Incident rejected.')
      load()
    } catch {
      notify.error('Failed to update incident.')
    }
  }

  return (
    <div>
      <h2 className="mb-4 text-lg font-semibold">Pending Verification</h2>
      <IncidentList incidents={incidents} isLoading={isLoading} onVerify={handleVerify} />
    </div>
  )
}
