function GlassCard({ children, className = '', hover = false }) {
  return (
    <div className={`panel ${hover ? 'panel-hover' : ''} ${className}`}>
      {children}
    </div>
  )
}

export default GlassCard