import { useEffect, useRef } from 'react'
import ChatBubble from './ChatBubble.jsx'
import ChatInput from './ChatInput.jsx'
import { useChatStore } from '../../store/useChatStore.js'
import { notify } from '../common/Toast.jsx'

export default function ChatWindow() {
  const { messages, sendMessage, isSending } = useChatStore()
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (message) => {
    try {
      await sendMessage(message)
    } catch {
      notify.error('The assistant is temporarily unavailable.')
    }
  }

  return (
    <div className="flex h-[70vh] flex-col rounded-xl border border-slate-200 bg-white">
      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.length === 0 && (
          <p className="text-sm text-slate-400">
            Ask about first aid, evacuation steps, or shelter-in-place guidance. For life-threatening
            emergencies, contact local emergency services immediately.
          </p>
        )}
        {messages.map((m, idx) => (
          <ChatBubble key={idx} role={m.role} content={m.content} />
        ))}
        <div ref={bottomRef} />
      </div>
      <ChatInput onSend={handleSend} disabled={isSending} />
    </div>
  )
}
