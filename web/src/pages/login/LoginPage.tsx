import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(username, password)
      navigate('/map', { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo">
          {/* swap for your logo */}
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#1a56db" />
            <path d="M8 16h16M16 8v16" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" />
          </svg>
        </div>

        <h1>Welkom terug</h1>
        <p className="login-subtitle">Log in op KabelLeiding</p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="username">Gebruikersnaam</label>
            <input
              id="username"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="field">
            <label htmlFor="password">Wachtwoord</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          {error && <p className="login-error">{error}</p>}

          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? 'Inloggen…' : 'Inloggen'}
          </button>
        </form>
      </div>

      <style>{`
        .login-page {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #f4f5f7;
        }
        .login-card {
          background: #fff;
          border-radius: 12px;
          box-shadow: 0 1px 4px rgba(0,0,0,.08), 0 4px 24px rgba(0,0,0,.06);
          padding: 2.5rem 2rem;
          width: 100%;
          max-width: 380px;
          text-align: center;
        }
        .login-logo { margin-bottom: 1.25rem; }
        .login-card h1 {
          font-size: 1.35rem;
          font-weight: 600;
          margin: 0 0 .25rem;
          color: #111;
        }
        .login-subtitle {
          font-size: .875rem;
          color: #6b7280;
          margin: 0 0 1.75rem;
        }
        .field {
          text-align: left;
          margin-bottom: 1rem;
        }
        .field label {
          display: block;
          font-size: .8125rem;
          font-weight: 500;
          color: #374151;
          margin-bottom: .375rem;
        }
        .field input {
          width: 100%;
          padding: .5rem .75rem;
          border: 1px solid #d1d5db;
          border-radius: 8px;
          font-size: .9375rem;
          outline: none;
          box-sizing: border-box;
          transition: border-color .15s;
        }
        .field input:focus { border-color: #1a56db; }
        .field input:disabled { background: #f9fafb; }
        .login-error {
          font-size: .8125rem;
          color: #dc2626;
          background: #fef2f2;
          border: 1px solid #fecaca;
          border-radius: 6px;
          padding: .5rem .75rem;
          margin: 0 0 1rem;
          text-align: left;
        }
        .login-btn {
          width: 100%;
          padding: .625rem;
          background: #1a56db;
          color: #fff;
          border: none;
          border-radius: 8px;
          font-size: .9375rem;
          font-weight: 500;
          cursor: pointer;
          transition: background .15s, opacity .15s;
        }
        .login-btn:hover:not(:disabled) { background: #1447c0; }
        .login-btn:disabled { opacity: .65; cursor: default; }
      `}</style>
    </div>
  )
}