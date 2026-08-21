import CapacityMeter from './CapacityMeter.jsx'

export default function ShelterCard({ shelter, onSelect }) {
  return (
    <button onClick={() => onSelect?.(shelter)} className="card block w-full text-left hover:shadow-md transition-shadow">
      <h3 className="font-semibold">{shelter.name}</h3>
      <p className="text-xs text-slate-500 mb-2">{shelter.address_text}</p>
      <CapacityMeter occupied={shelter.capacity_occupied} total={shelter.capacity_total} />
      <p className="mt-2 text-xs capitalize text-slate-400">{shelter.shelter_type.replace('_', ' ')} · {shelter.status}</p>
    </button>
  )
}
