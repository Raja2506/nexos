import { useState, useCallback, useRef } from 'react'

const WS_URL = 'ws://localhost:8000/ws/agent-run'
const STORAGE_KEY = 'nexos_run_history'

function saveRun(goal, completedAgents) {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const history = raw ? JSON.parse(raw) : []
    history.push({ goal, completedAgents, timestamp: Date.now() })
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(-50)))
  } catch {
    // localStorage unavailable - skip silently
  }
}

export function useLiveSocket() {
  const [completed, setCompleted] = useState([])
  const [running, setRunning] = useState(false)
  const [error, setError] = useState(null)
  const socketRef = useRef(null)
  const completedRef = useRef([])

  const run = useCallback((goal) => {
    if (!goal.trim()) return

    setCompleted([])
    completedRef.current = []
    setError(null)
    setRunning(true)

    const ws = new WebSocket(WS_URL)
    socketRef.current = ws

    ws.onopen = () => ws.send(JSON.stringify({ goal }))

    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data)
      if (data.type === 'agent_finished') {
        completedRef.current = [...completedRef.current, data.agent]
        setCompleted(completedRef.current)
      } else if (data.type === 'done') {
        setRunning(false)
        saveRun(goal, completedRef.current.length)
        ws.close()
      } else if (data.type === 'error') {
        setError(data.message)
        setRunning(false)
        saveRun(goal, completedRef.current.length)
        ws.close()
      }
    }

    ws.onerror = () => {
      setError('Connection failed')
      setRunning(false)
    }
  }, [])

  return { run, completed, running, error }
}
