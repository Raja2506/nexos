import { useState, useCallback, useRef } from 'react'

const WS_URL = 'ws://localhost:8000/ws/agent-run'

export function useLiveSocket() {
  const [completed, setCompleted] = useState([])
  const [running, setRunning] = useState(false)
  const [error, setError] = useState(null)
  const socketRef = useRef(null)

  const run = useCallback((goal) => {
    if (!goal.trim()) return

    setCompleted([])
    setError(null)
    setRunning(true)

    const ws = new WebSocket(WS_URL)
    socketRef.current = ws

    ws.onopen = () => ws.send(JSON.stringify({ goal }))

    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data)
      if (data.type === 'agent_finished') {
        setCompleted((prev) => [...prev, data.agent])
      } else if (data.type === 'done') {
        setRunning(false)
        ws.close()
      } else if (data.type === 'error') {
        setError(data.message)
        setRunning(false)
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