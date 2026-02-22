import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface DatabaseConfig {
  host: string;
  port: string;
  user: string;
  database: string;
  schema: string;
}

interface ScoutState {
  // Connection State
  dbConfig: DatabaseConfig | null;
  isConnected: boolean;
  selectedSchemas: string | string[];
  
  // Analysis Results
  ragCorpusId: string | null;
  mdGcsPath: string | null;
  jsonGcsPath: string | null;
  previewTables: string[];
  
  // Session State
  sessionId: string | null;
  
  // Actions
  setDbConfig: (config: DatabaseConfig) => void;
  setConnected: (status: boolean) => void;
  setSelectedSchemas: (schemas: string | string[]) => void;
  setAnalysisResults: (results: {
    rag_corpus_id: string;
    md_gcs_path: string;
    json_gcs_path: string;
    preview_tables: string[];
  }) => void;
  setSessionId: (id: string) => void;
  reset: () => void;
}

export const useScoutStore = create<ScoutState>()(
  persist(
    (set) => ({
      dbConfig: null,
      isConnected: false,
      selectedSchemas: 'public',
      ragCorpusId: null,
      mdGcsPath: null,
      jsonGcsPath: null,
      previewTables: [],
      sessionId: null,

      setDbConfig: (config) => set({ dbConfig: config }),
      setConnected: (status) => set({ isConnected: status }),
      setSelectedSchemas: (schemas) => set({ selectedSchemas: schemas }),
      setAnalysisResults: (results) => set({
        ragCorpusId: results.rag_corpus_id,
        mdGcsPath: results.md_gcs_path,
        jsonGcsPath: results.json_gcs_path,
        previewTables: results.preview_tables,
      }),
      setSessionId: (id) => set({ sessionId: id }),
      reset: () => set({
        dbConfig: null,
        isConnected: false,
        selectedSchemas: 'public',
        ragCorpusId: null,
        mdGcsPath: null,
        jsonGcsPath: null,
        previewTables: [],
        sessionId: null,
      }),
    }),
    {
      name: 'db-scout-storage',
    }
  )
);
