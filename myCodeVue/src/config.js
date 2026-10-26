
const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080';
export const API_BASE_URL = rawUrl.startsWith('http') 
  ? rawUrl.replace(/\/+$/, '') 
  : `https://${rawUrl}`.replace(/\/+$/, '');