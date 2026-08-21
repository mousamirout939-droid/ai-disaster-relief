import clsx from 'clsx'

export default function CapacityMeter({ occupied, total }) {
  const pct = total > 0 ? Math.min(100, Math.round((occupied / total) * 100)) : 0
  const colorClass = pct >= 90 ? 'bg-red-500' : pct >= 70 ? 'bg-amber-500' : 'bg-green-500'
  return (
    <div>
      <div className="mb-1 flex justify-between text-xs text-slate-500">
        <span>Capacity</span>
        <span>{occupied}/{total}</span>
      </div>
      <div className="h-2 w-full rounded-full bg-slate-200">
        <div className={clsx('h-2 rounded-full', colorClass)} style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}
