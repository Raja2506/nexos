import { useState } from 'react'
import { useLiveSocket } from '../hooks/useLiveSocket'
import DAGNode from '../components/DAGNode'
import GlassCard from '../components/GlassCard'

const NODES = [
  { key: 'plan_node', label: 'Planner', x: 100, y: 150 },
  { key: 'decide_task_type_node', label: 'Decision', x: 300, y: 150 },
  { key: 'sql_node', label: 'SQL', x: 500, y: 80 },
  { key: 'clean_data_node', label: 'Data Clean', x: 650, y: 80 },
  { key: 'qa_node', label: 'QA', x: 800, y: 80 },
  { key: 'report_node', label: 'Report', x: 950, y: 150 },
]

const EDGES = [
  { from: 'plan_node', to: 'decide_task_type_node' },
  { from: 'decide_task_type_node', to: 'sql_node' },
  { from: 'sql_node', to: 'clean_data_node' },
  { from: 'clean_data_node', to: 'qa_node' },
  { from: 'qa_node', to: 'report_node' },
  { from: 'decide_task_type_node', to: 'report_node' },
]

function findNode(key) {
  return NODES.find((n) => n.key === key)
}

function WorkflowGraph() {
  const [goal, setGoal] = useState('')
  const { run, completed, running } = useLiveSocket()

  // An edge only lights up if "to" ran IMMEDIATELY after "from"
  // in the actual execution order - not just "both happen to be done".
  const isEdgeActive = (edge) => {
    const fromIndex = completed.indexOf(edge.from)
    const toIndex = completed.indexOf(edge.to)
    if (fromIndex === -1 || toIndex === -1) return false
    return toIndex === fromIndex + 1
  }

  return (
    <div className="max-w-5xl mx-auto w-full">
      <h1 className="font-display text-4xl font-bold mb-2">Workflow Graph</h1>
      <p className="text-[var(--ghost-dim)] mb-6 font-mono text-sm">
        $ live topology of the LangGraph orchestration
      </p>

      <div className="flex gap-2 mb-6">
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

      <GlassCard className="p-6 relative overflow-x-auto">
        <div className="relative" style={{ width: 1050, height: 260 }}>
          <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 0 }}>
            {EDGES.map((edge, i) => {
              const from = findNode(edge.from)
              const to = findNode(edge.to)
              const active = isEdgeActive(edge)
              return (
                <line
                  key={i}
                  x1={from.x + 48}
                  y1={from.y}
                  x2={to.x - 48}
                  y2={to.y}
                  stroke={active ? '#00D9B5' : '#2A2E38'}
                  strokeWidth={active ? 2.5 : 1.5}
                  style={{ transition: 'stroke 0.4s ease' }}
                />
              )
            })}
          </svg>

          <div className="absolute inset-0" style={{ zIndex: 1 }}>
            {NODES.map((node, i) => {
              const isDone = completed.includes(node.key)
              const isActive = !isDone && i === completed.length && running
              return (
                <DAGNode
                  key={node.key}
                  x={node.x}
                  y={node.y}
                  label={node.label}
                  status={isDone ? 'done' : isActive ? 'active' : 'pending'}
                />
              )
            })}
          </div>
        </div>
      </GlassCard>

      <p className="mt-4 font-mono text-xs text-[var(--ghost-dim)]">
        note: Decision branches directly to Report when no data lookup is needed.
      </p>
    </div>
  )
}

export default WorkflowGraph
