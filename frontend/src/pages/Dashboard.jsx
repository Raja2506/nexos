import { useState, useEffect } from 'react'
import GlassCard from '../components/GlassCard'

const STORAGE_KEY = 'nexos_run_history'

function loadHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function StatCard({ label, value }) {
  return (
    <GlassCard className="p-5 flex-1">
      <p className="font-mono text-xs text-[var(--ghost-dim)] mb-1">{label}</p>
      <p className="font-display text-3xl font-bold">{value}</p>
    </GlassCard>
  )
}

function Dashboard() {
  const [history, setHistory] = useState([])

  useEffect(() => {
    setHistory(loadHistory())
    const onFocus = () => setHistory(loadHistory())
    window.addEventListener('focus', onFocus)
    return () => window.removeEventListener('focus', onFocus)
  }, [])

  const totalRuns = history.length
  const completedRuns = history.filter((r) => r.completedAgents === 6).length
  const successRate = totalRuns ? Math.round((completedRuns / totalRuns) * 100) : 0
  const avgAgents = totalRuns
    ? (history.reduce((sum, r) => sum + r.completedAgents, 0) / totalRuns).toFixed(1)
    : '0'

  return (
    <div className="max-w-4xl mx-auto w-full">
      <h1 className="font-display text-4xl font-bold mb-2">Dashboard</h1>
      <p className="text-[var(--ghost-dim)] mb-8 font-mono text-sm">
        session analytics - runs executed on this browser
      </p>

      <div className="flex gap-4 mb-8">
        <StatCard label="TOTAL RUNS" value={totalRuns} />
        <StatCard label="SUCCESS RATE" value={`${successRate}%`} />
        <StatCard label="AVG AGENTS/RUN" value={avgAgents} />
      </div>

      <GlassCard className="p-6">
        <h2 className="font-display font-bold mb-4">Recent Runs</h2>
        {history.length === 0 ? (
          <p className="font-mono text-sm text-[var(--ghost-dim)]">
            No runs yet - go to Workspace and execute a goal.
          </p>
        ) : (
          <div className="space-y-2">
            {[...history].reverse().slice(0, 10).map((run, i) => (
              <div
                key={i}
                className="flex items-center justify-between panel px-4 py-3 text-sm"
              >
                <span className="font-mono truncate max-w-xs">{run.goal}</span>
                <span className="font-mono text-[var(--ghost-dim)]">
                  {run.completedAgents}/6 agents
                </span>
                <span
                  className={`font-mono text-xs ${
                    run.completedAgents === 6 ? 'text-[var(--circuit)]' : 'text-[var(--signal)]'
                  }`}
                >
                  {run.completedAgents === 6 ? 'COMPLETE' : 'PARTIAL'}
                </span>
              </div>
            ))}
          </div>
        )}
      </GlassCard>
    </div>
  )
}

export default Dashboard
