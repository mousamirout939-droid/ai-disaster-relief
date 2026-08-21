import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import ImageUploader from './ImageUploader.jsx'
import Button from '../common/Button.jsx'
import { useIncidentStore } from '../../store/useIncidentStore.js'
import { useGeolocation } from '../../hooks/useGeolocation.js'
import { notify } from '../common/Toast.jsx'

const schema = z.object({
  category: z.enum(['flood', 'fire', 'earthquake', 'hurricane', 'landslide', 'building_collapse', 'medical_emergency', 'other']),
  description: z.string().min(5, 'Please describe what you observed (min 5 characters).'),
  address_text: z.string().optional(),
})

export default function IncidentForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({ resolver: zodResolver(schema) })
  const { location } = useGeolocation()
  const submitReport = useIncidentStore((s) => s.submitReport)
  let images = []

  const onSubmit = async (values) => {
    if (!location) {
      notify.error('We need your location to submit a report. Please enable GPS.')
      return
    }
    const formData = new FormData()
    formData.append('category', values.category)
    formData.append('description', values.description)
    formData.append('longitude', location.lng)
    formData.append('latitude', location.lat)
    if (values.address_text) formData.append('address_text', values.address_text)
    images.forEach((file) => formData.append('images', file))

    try {
      await submitReport(formData)
      notify.success('Incident reported. Nearby volunteers have been notified.')
    } catch {
      notify.error('Failed to submit report. Please try again.')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="card space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium">Disaster Type</label>
        <select {...register('category')} className="input-field">
          <option value="flood">Flood</option>
          <option value="fire">Fire</option>
          <option value="earthquake">Earthquake</option>
          <option value="hurricane">Hurricane</option>
          <option value="landslide">Landslide</option>
          <option value="building_collapse">Building Collapse</option>
          <option value="medical_emergency">Medical Emergency</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium">What's happening?</label>
        <textarea {...register('description')} rows={3} className="input-field" placeholder="Describe the situation..." />
        {errors.description && <p className="mt-1 text-xs text-red-600">{errors.description.message}</p>}
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium">Address (optional)</label>
        <input {...register('address_text')} className="input-field" placeholder="Nearest cross street or landmark" />
      </div>

      <ImageUploader onChange={(files) => { images = files }} />

      <p className="text-xs text-slate-400">
        📍 {location ? `Location detected (${location.lat.toFixed(4)}, ${location.lng.toFixed(4)})` : 'Detecting your location...'}
      </p>

      <Button type="submit" variant="danger" disabled={isSubmitting} className="w-full">
        {isSubmitting ? 'Submitting...' : 'Submit Emergency Report'}
      </Button>
    </form>
  )
}
