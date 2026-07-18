import { useLiveSocket } from '../hooks/useLiveSocket'
import AgentNode from '../components/AgentNode'
import GlassCard from '../components/GlassCard'
import { useState } from 'react'

const PIPELINE = [
  { key: 'plan_node', label: 'Planner' },
  { key: 'decide_task_type_node', label: 'Decision' },
  { key: 'sql_node', label: 'SQL' },
  { key: 'clean_data_node', label: 'Data Clean' },
  { key: 'qa_node', label: 'QA' },
  { key: 'report_node', label: 'Report' },
]

function Workspace() {
  const [goal, setGoal] = useState('')
  const { run, completed, running, error } = useLiveSocket()

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="font-display text-4xl font-bold mb-2">Agent Console</h1>
      <p className="text-[var(--ghost-dim)] mb-8 font-mono text-sm">
        $ describe a goal, watch the pipeline execute
      </p>

      <div className="flex gap-2 mb-10">
        <input
          className="panel flex-1 px-4 py-3 bg-transparent outline-none font-mono text-sm placeholder-white/30 focus:border-[var(--circuit)] transition"
          placeholder="how many tasks are there in total?"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && run(goal)}
        />
        <button
          onClick={() => run(goal)}
          disabled={running}
          className="px-6 py-3 rounded-[8px] font-display font-bold text-sm bg-[var(--circuit)] text-[var(--void)] hover:brightness-110 transition disabled:opacity-30"
        >
          {running ? 'RUNNING' : 'EXECUTE'}
        </button>
      </div>

      <GlassCard className="p-8">
        <div className="flex items-center">
          {PIPELINE.map((agent, i) => {
            const isDone = completed.includes(agent.key)
            const isActive = !isDone && i === completed.length && running
            return (
              <div key={agent.key} className="flex items-center flex-1 last:flex-none">
                <AgentNode
                  label={agent.label}
                  index={i + 1}
                  status={isDone ? 'done' : isActive ? 'active' : 'pending'}
                />
                {i < PIPELINE.length - 1 && (
                  <div className={`trace flex-1 mx-1 ${isDone ? 'active' : ''}`} />
                )}
              </div>
            )
          })}
        </div>
      </GlassCard>

      {error && (
        <GlassCard className="mt-4 p-4 border-[var(--danger)]">
          <span className="font-mono text-sm text-[var(--danger)]">ERROR: {error}</span>
        </GlassCard>
      )}
    </div>
  )
}

export default Workspace