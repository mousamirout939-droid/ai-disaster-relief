import { useForm } from 'react-hook-form'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { notify } from '../components/common/Toast.jsx'
import Button from '../components/common/Button.jsx'

export default function LoginPage() {
  const { register, handleSubmit, formState: { isSubmitting } } = useForm()
  const { login } = useAuth()
  const navigate = useNavigate()

  const onSubmit = async (values) => {
    try {
      await login(values.email, values.password)
      navigate('/dashboard')
    } catch {
      notify.error('Invalid email or password.')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 px-4">
      <form onSubmit={handleSubmit(onSubmit)} className="card w-full max-w-sm space-y-4">
        <h1 className="text-xl font-bold">Welcome back</h1>
        <input {...register('email', { required: true })} type="email" placeholder="Email" className="input-field" />
        <input {...register('password', { required: true })} type="password" placeholder="Password" className="input-field" />
        <Button type="submit" disabled={isSubmitting} className="w-full">{isSubmitting ? 'Logging in...' : 'Log In'}</Button>
        <p className="text-center text-sm text-slate-500">
          No account? <Link to="/register" className="text-brand-700 hover:underline">Register</Link>
        </p>
      </form>
    </div>
  )
}
