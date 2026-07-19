function DAGNode({ x, y, label, status }) {
  const stateClass = status === 'done' ? 'active' : status === 'active' ? 'warn animate-pulse' : ''

  return (
    <div
      className={`node absolute flex flex-col items-center justify-center w-24 h-16 -translate-x-1/2 -translate-y-1/2 ${stateClass}`}
      style={{ left: x, top: y }}
    >
      <span className="font-mono text-[11px] font-semibold">{label}</span>
      {status === 'done' && <span className="text-[var(--circuit)] text-[10px]">OK</span>}
    </div>
  )
}

export default DAGNode
