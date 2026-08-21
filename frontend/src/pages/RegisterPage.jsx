import { useForm } from 'react-hook-form'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { notify } from '../components/common/Toast.jsx'
import Button from '../components/common/Button.jsx'

export default function RegisterPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm()
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (values) => {
    try {
      await registerUser(values)
      navigate('/dashboard')
    } catch {
      notify.error('Registration failed. Please check your details.')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <form onSubmit={handleSubmit(onSubmit)} className="card w-full max-w-sm space-y-4">
        <h1 className="text-xl font-bold">Create your account</h1>
        <input {...register('full_name', { required: true })} placeholder="Full name" className="input-field" />
        <input {...register('email', { required: true })} type="email" placeholder="Email" className="input-field" />
        <input {...register('password', { required: true, minLength: 8 })} type="password" placeholder="Password (min 8 chars)" className="input-field" />
        <input {...register('phone')} placeholder="Phone (optional)" className="input-field" />
        <select {...register('role')} className="input-field">
          <option value="citizen">Citizen</option>
          <option value="volunteer">Volunteer (requires admin approval)</option>
        </select>
        <Button type="submit" disabled={isSubmitting} className="w-full">{isSubmitting ? 'Creating...' : 'Register'}</Button>
        <p className="text-center text-sm text-slate-500">
          Already have an account? <Link to="/login" className="text-brand-700 hover:underline">Log In</Link>
        </p>
      </form>
    </div>
  )
}
