/**
 * API Client Utilities
 * Centralized HTTP client for FastAPI backend communication
 */

import { API_BASE_URL, API_ENDPOINTS, getApiUrl } from './config';

interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
}

interface DatabaseTestPayload {
  config: {
    host: string;
    port: string;
    user: string;
    password: string;
    database: string;
    schema: string;
  };
}

interface SchemaResponse {
  status: string;
  schemas: string[];
  count?: number;
}

interface AnalysisRunPayload {
  user_id: string;
  schema_name: string | string[];
}

interface AnalysisRunResponse {
  status: string;
  json_gcs_path: string;
  md_gcs_path: string;
  rag_corpus_id: string;
  preview_tables: string[];
}

interface ChatPayload {
  query: string;
  rag_corpus_id: string;
  session_id: string;
}

interface ChatResponse {
  response: string;
}

/**
 * Test database connection
 */
export const testDatabaseConnection = async (payload: DatabaseTestPayload): Promise<ApiResponse<any>> => {
  try {
    const response = await fetch(getApiUrl(API_ENDPOINTS.database.test), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    return {
      status: 'error',
      message: `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
};

/**
 * Fetch available schemas from database
 */
export const fetchDatabaseSchemas = async (): Promise<SchemaResponse | null> => {
  try {
    const response = await fetch(getApiUrl(API_ENDPOINTS.database.schemas), {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch schemas:', error);
    return null;
  }
};

/**
 * Run agentic scout analysis
 */
export const runAnalysis = async (payload: AnalysisRunPayload): Promise<AnalysisRunResponse | null> => {
  try {
    const response = await fetch(getApiUrl(API_ENDPOINTS.analysis.run), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to run analysis:', error);
    return null;
  }
};

/**
 * Send chat query to scout agent
 */
export const sendChatMessage = async (payload: ChatPayload): Promise<ChatResponse | null> => {
  try {
    const response = await fetch(getApiUrl(API_ENDPOINTS.chat), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to send chat message:', error);
    return null;
  }
};

/**
 * Fetch file from GCS path (via backend proxy if private)
 */
export const fetchGcsFile = async (gcsPath: string): Promise<string | null> => {
  try {
    // We use the new /download proxy on port 8000 (vite proxy configured for '/download')
    // encodeURIComponent is critical because the path contains slashes and special characters
    const response = await fetch(`/download?path=${encodeURIComponent(gcsPath)}`);
    
    if (!response.ok) {
      console.error(`Failed to fetch GCS file: ${response.statusText}`);
      return null;
    }

    // Returns the raw text (Markdown) from our backend proxy
    return await response.text();
  } catch (error) {
    console.error("Network error fetching GCS file:", error);
    return null;
  }
};
