function Placeholder({ title, note }) {
  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="font-display text-4xl font-bold mb-2">{title}</h1>
      <p className="font-mono text-sm text-[var(--ghost-dim)]">$ {note}</p>
    </div>
  )
}

export default Placeholder