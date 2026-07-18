import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Workspace from './pages/Workspace'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import AgentTimeline from './pages/AgentTimeline'
import MemoryInspector from './pages/MemoryInspector'
import WorkflowGraph from './pages/WorkflowGraph'

const NAV_ITEMS = [
  { to: '/', label: 'Workspace' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/timeline', label: 'Timeline' },
  { to: '/memory', label: 'Memory' },
  { to: '/graph', label: 'Graph' },
]

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <header className="border-b border-[var(--wire)] px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="status-dot" />
            <span className="font-display font-bold text-lg tracking-tight">NexOS</span>
          </div>
          <nav className="flex gap-1 font-mono text-xs">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `px-3 py-1.5 rounded-md transition ${
                    isActive
                      ? 'bg-[var(--panel)] text-[var(--circuit)] border border-[var(--circuit)]'
                      : 'text-[var(--ghost-dim)] hover:text-[var(--ghost)]'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </header>

        <main className="flex-1 p-6 flex items-center justify-center">
          <Routes>
            <Route path="/" element={<Workspace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/login" element={<Login />} />
            <Route path="/timeline" element={<AgentTimeline />} />
            <Route path="/memory" element={<MemoryInspector />} />
            <Route path="/graph" element={<WorkflowGraph />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App