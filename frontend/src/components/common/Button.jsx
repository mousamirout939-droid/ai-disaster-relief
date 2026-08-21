import clsx from 'clsx'

export default function Button({ variant = 'primary', className, children, ...props }) {
  const base = 'inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed'
  const variants = {
    primary: 'bg-brand-700 text-white hover:bg-brand-900',
    danger: 'bg-emergency-critical text-white hover:bg-red-700',
    outline: 'border border-slate-300 text-slate-700 hover:bg-slate-50',
    ghost: 'text-slate-600 hover:bg-slate-100',
  }
  return (
    <button className={clsx(base, variants[variant], className)} {...props}>
      {children}
    </button>
  )
}
