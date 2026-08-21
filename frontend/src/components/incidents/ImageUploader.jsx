import { useRef, useState } from 'react'

export default function ImageUploader({ onChange, maxFiles = 5 }) {
  const inputRef = useRef(null)
  const [previews, setPreviews] = useState([])

  const handleFiles = (fileList) => {
    const files = Array.from(fileList).slice(0, maxFiles)
    setPreviews(files.map((f) => URL.createObjectURL(f)))
    onChange(files)
  }

  return (
    <div className="space-y-2">
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        className="w-full rounded-lg border-2 border-dashed border-slate-300 py-6 text-sm text-slate-500 hover:border-brand-500"
      >
        📷 Tap to add photos of the disaster (up to {maxFiles})
      </button>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        multiple
        hidden
        onChange={(e) => handleFiles(e.target.files)}
      />
      {previews.length > 0 && (
        <div className="flex gap-2 overflow-x-auto">
          {previews.map((src) => (
            <img key={src} src={src} alt="preview" className="h-20 w-20 rounded-lg object-cover" />
          ))}
        </div>
      )}
    </div>
  )
}
