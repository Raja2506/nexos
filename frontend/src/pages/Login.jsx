import { useEffect, useRef, useState } from 'react'
import GlassCard from '../components/GlassCard'

const API_URL = 'http://localhost:8000'

function Login() {
  const buttonRef = useRef(null)
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState(null)
  const googleClientId = (window.__GOOGLE_CLIENT_ID__ || import.meta.env.VITE_GOOGLE_CLIENT_ID || '953636665044-soop4pnc7pn7pke4cga26u3eo3jcgt3f.apps.googleusercontent.com').trim()

  useEffect(() => {
    if (!googleClientId) {
      setError('Google client ID is not configured.')
      return
    }

    let cancelled = false

    const initializeGoogleButton = () => {
      if (!window.google?.accounts?.id) {
        window.setTimeout(initializeGoogleButton, 200)
        return
      }

      if (cancelled) return

      window.google.accounts.id.initialize({
        client_id: googleClientId,
        callback: handleGoogleResponse,
      })

      window.google.accounts.id.renderButton(buttonRef.current, {
        theme: 'filled_black',
        size: 'large',
        shape: 'pill',
      })
    }

    initializeGoogleButton()

    return () => {
      cancelled = true
    }
  }, [googleClientId])

  const handleGoogleResponse = async (response) => {
    setStatus('verifying')
    setError(null)

    try {
      const res = await fetch(`${API_URL}/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_token: response.credential }),
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Login failed')
      }

      const data = await res.json()
      localStorage.setItem('nexos_token', data.access_token)
      setStatus('success')
    } catch (err) {
      setError(err.message)
      setStatus('idle')
    }
  }

  return (
    <div className="max-w-md mx-auto w-full">
      <GlassCard className="p-8 text-center">
        <h1 className="font-display text-3xl font-bold mb-2">Sign In</h1>
        <p className="font-mono text-sm text-[var(--ghost-dim)] mb-8">
          $ authenticate to access NexOS
        </p>

        <div ref={buttonRef} className="flex justify-center mb-4" />

        {status === 'verifying' && (
          <p className="font-mono text-xs text-[var(--signal)]">Verifying...</p>
        )}
        {status === 'success' && (
          <p className="font-mono text-xs text-[var(--circuit)]">Signed in successfully!</p>
        )}
        {error && (
          <p className="font-mono text-xs text-[var(--danger)]">{error}</p>
        )}
      </GlassCard>
    </div>
  )
}

export default Login
