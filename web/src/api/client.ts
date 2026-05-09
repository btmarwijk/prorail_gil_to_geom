import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000', // Points to your FastAPI container port
});

const TOKEN_KEY = 'auth_token'

export async function apiFetch(input: RequestInfo, init: RequestInit = {}) {
  const token = localStorage.getItem(TOKEN_KEY)
  return fetch(input, {
    ...init,
    headers: {
      ...(init.headers ?? {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })
}