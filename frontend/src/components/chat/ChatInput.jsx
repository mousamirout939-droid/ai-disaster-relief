import { useState } from 'react'

export default function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState('')

  const submit = () => {
    if (!value.trim()) return
    onSend(value.trim())
    setValue('')
  }

  return (
    <div className="flex gap-2 border-t border-slate-200 p-3">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && submit()}
        placeholder="Ask the AI emergency assistant..."
        className="input-field flex-1"
        disabled={disabled}
      />
      <button onClick={submit} disabled={disabled} className="btn-primary">Send</button>
    </div>
  )
}
