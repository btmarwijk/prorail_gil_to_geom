import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  type ReactNode,
} from 'react'

interface AuthUser {
  username: string
  email?: string
}

interface AuthContextValue {
  user: AuthUser | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

// Set VITE_BYPASS_AUTH=true in .env.development to skip login during dev
const BYPASS_AUTH = import.meta.env.VITE_BYPASS_AUTH === 'true'
const DEV_USER: AuthUser = { username: 'dev', email: 'dev@local' }
const TOKEN_KEY = 'auth_token'

const AuthContext = createContext<AuthContextValue | null>(null)

function parseJwtPayload(token: string): AuthUser | null {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return {
      username: payload.sub ?? payload.username ?? 'user',
      email: payload.email,
    }
  } catch {
    return null
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<AuthUser | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Rehydrate from localStorage on mount
  useEffect(() => {
    if (BYPASS_AUTH) {
      setUser(DEV_USER)
      setIsLoading(false)
      return
    }
    const stored = localStorage.getItem(TOKEN_KEY)
    if (stored) {
      const parsed = parseJwtPayload(stored)
      if (parsed) {
        setToken(stored)
        setUser(parsed)
      } else {
        localStorage.removeItem(TOKEN_KEY)
      }
    }
    setIsLoading(false)
  }, [])

  const login = useCallback(async (username: string, password: string) => {
    // FastAPI's OAuth2PasswordRequestForm expects form-encoded data
    const form = new URLSearchParams()
    form.append('username', username)
    form.append('password', password)

    const res = await fetch('/api/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString(),
    })

    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err?.detail ?? 'Login failed')
    }

    const data: { access_token: string; token_type: string } = await res.json()
    const parsed = parseJwtPayload(data.access_token)
    if (!parsed) throw new Error('Invalid token received')

    localStorage.setItem(TOKEN_KEY, data.access_token)
    setToken(data.access_token)
    setUser(parsed)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: BYPASS_AUTH ? true : !!user,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}