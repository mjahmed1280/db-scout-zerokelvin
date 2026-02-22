/**
 * API Configuration
 * Centralized configuration for FastAPI backend connections
 */

// FastAPI Backend URL
// Use Vite env (import.meta.env) which is available in the browser at build/runtime
const VITE_API_URL = (import.meta as any).env?.VITE_API_URL;
export const API_BASE_URL = VITE_API_URL || 'http://localhost:8000';

// API Endpoints
export const API_ENDPOINTS = {
  // Database Endpoints
  database: {
    test: '/database/test',
    schemas: '/database/schemas',
  },
  // Analysis Endpoints
  analysis: {
    run: '/analysis/run',
  },
  // Chat Endpoints
  chat: '/chat',
} as const;

// Helper to construct full API URLs
export const getApiUrl = (endpoint: string): string => {
  return `${API_BASE_URL}${endpoint}`;
};
