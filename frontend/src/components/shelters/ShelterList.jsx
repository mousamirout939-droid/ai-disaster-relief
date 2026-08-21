import ShelterCard from './ShelterCard.jsx'
import Loader from '../common/Loader.jsx'

export default function ShelterList({ shelters, isLoading, onSelect }) {
  if (isLoading) return <Loader label="Finding nearby shelters..." />
  if (!shelters.length) return <p className="text-sm text-slate-400">No shelters found in this area.</p>
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {shelters.map((shelter) => (
        <ShelterCard key={shelter.id} shelter={shelter} onSelect={onSelect} />
      ))}
    </div>
  )
}
