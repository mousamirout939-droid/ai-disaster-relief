import clsx from 'clsx'

export default function ChatBubble({ role, content }) {
  const isUser = role === 'user'
  return (
    <div className={clsx('flex', isUser ? 'justify-end' : 'justify-start')}>
      <div
        className={clsx(
          'max-w-[75%] rounded-2xl px-4 py-2 text-sm',
          isUser ? 'bg-brand-700 text-white rounded-br-sm' : 'bg-slate-100 text-slate-800 rounded-bl-sm',
        )}
      >
        {content}
      </div>
    </div>
  )
}
