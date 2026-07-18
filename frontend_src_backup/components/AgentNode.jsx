function AgentNode({ label, status, index }) {
  // status: 'pending' | 'active' | 'done'
  const stateClass = status === 'done' ? 'active' : status === 'active' ? 'warn animate-pulse' : ''

  return (
    <div className="flex flex-col items-center gap-2">
      <div className={`node w-14 h-14 flex items-center justify-center font-mono text-[10px] ${stateClass}`}>
        {status === 'done' ? '✓' : index}
      </div>
      <span className="font-mono text-[10px] text-[var(--ghost-dim)] text-center w-16">
        {label}
      </span>
    </div>
  )
}

export default AgentNode