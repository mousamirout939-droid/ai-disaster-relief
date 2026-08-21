import clsx from 'clsx'

const STYLES = {
  low: 'bg-lime-100 text-lime-800',
  moderate: 'bg-amber-100 text-amber-800',
  high: 'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
}

export default function SeverityBadge({ severity }) {
  return (
    <span className={clsx('inline-block rounded-full px-2 py-0.5 text-xs font-semibold capitalize', STYLES[severity])}>
      {severity}
    </span>
  )
}
