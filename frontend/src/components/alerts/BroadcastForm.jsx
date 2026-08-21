import { useForm } from 'react-hook-form'
import { alertApi } from '../../api/alertApi.js'
import { notify } from '../common/Toast.jsx'
import Button from '../common/Button.jsx'

export default function BroadcastForm() {
  const { register, handleSubmit, reset, formState: { isSubmitting } } = useForm()

  const onSubmit = async (values) => {
    try {
      await alertApi.broadcast({
        title: values.title,
        message: values.message,
        severity: values.severity,
        radius_km: values.radius_km ? Number(values.radius_km) : undefined,
      })
      notify.success('Alert broadcast sent.')
      reset()
    } catch {
      notify.error('Failed to broadcast alert.')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="card space-y-3">
      <h3 className="font-semibold">Broadcast Emergency Alert</h3>
      <input {...register('title', { required: true })} placeholder="Alert title" className="input-field" />
      <textarea {...register('message', { required: true })} placeholder="Alert message" rows={3} className="input-field" />
      <select {...register('severity')} className="input-field">
        <option value="info">Info</option>
        <option value="warning">Warning</option>
        <option value="critical">Critical</option>
      </select>
      <input {...register('radius_km')} placeholder="Radius in km (leave blank for platform-wide)" className="input-field" />
      <Button type="submit" variant="danger" disabled={isSubmitting} className="w-full">
        {isSubmitting ? 'Sending...' : 'Broadcast Alert'}
      </Button>
    </form>
  )
}
