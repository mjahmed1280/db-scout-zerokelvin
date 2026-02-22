import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Database, Server, User, Lock, Globe, ChevronRight, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { useScoutStore } from './store';
import { useNavigate } from 'react-router-dom';
import { testDatabaseConnection, fetchDatabaseSchemas } from './api';

const DB_TYPES = [
  { id: 'postgres', name: 'PostgreSQL', icon: '🐘', active: true },
  { id: 'mysql', name: 'MySQL', icon: '🐬', active: false },
  { id: 'sqlserver', name: 'SQL Server', icon: '🗄️', active: false },
  { id: 'mongodb', name: 'MongoDB', icon: '🍃', active: false },
  { id: 'snowflake', name: 'Snowflake', icon: '❄️', active: false },
];

export default function Gateway() {
  const navigate = useNavigate();
  const { setDbConfig, setConnected, isConnected, setSelectedSchemas } = useScoutStore();
  const [selectedType, setSelectedType] = useState('postgres');
  const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');
  const [showSchemaSelection, setShowSchemaSelection] = useState(false);
  const [availableSchemas, setAvailableSchemas] = useState<string[]>([]);
  const [selectedSchemaList, setSelectedSchemaList] = useState<string[]>(['public']);
  const [fetchingSchemas, setFetchingSchemas] = useState(false);
  
  const [formData, setFormData] = useState({
    host: '',
    port: '5432',
    user: '',
    password: '',
    database: '',
    schema: 'public'
  });

  const handleTestConnection = async () => {
    setTestStatus('testing');
    setErrorMessage('');
    try {
      const response = await testDatabaseConnection({ config: formData });
      
      if (response.status === 'success') {
        setTestStatus('success');
        setConnected(true);
        setDbConfig(formData);
        fetchSchemas();
      } else {
        setTestStatus('error');
        setErrorMessage(response.message || 'Connection failed');
      }
    } catch (err) {
      setTestStatus('error');
      setErrorMessage('Network error occurred');
    }
  };

  const fetchSchemas = async () => {
    setFetchingSchemas(true);
    try {
      const response = await fetchDatabaseSchemas();
      if (response && response.status === 'success') {
        setAvailableSchemas(response.schemas);
        setSelectedSchemaList([response.schemas[0]]); // Default to first schema
        setShowSchemaSelection(true);
      } else {
        setErrorMessage('Failed to fetch schemas from database');
        setTestStatus('error');
      }
    } catch (err) {
      setErrorMessage('Network error fetching schemas');
      setTestStatus('error');
    } finally {
      setFetchingSchemas(false);
    }
  };

  const toggleSchema = (schema: string) => {
    setSelectedSchemaList(prev => 
      prev.includes(schema) 
        ? prev.filter(s => s !== schema) 
        : [...prev, schema]
    );
  };

  const handleDeploy = () => {
    const finalSchemas = selectedSchemaList.length === 1 ? selectedSchemaList[0] : selectedSchemaList;
    setSelectedSchemas(finalSchemas);
    navigate('/scouting');
  };

  return (
    <div className="min-h-screen bg-cyber-black flex flex-col items-center justify-center p-6">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl w-full"
      >
        <header className="text-center mb-12">
          <motion.h1 
            className="text-5xl font-bold tracking-tighter text-cyber-accent mb-2"
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
          >
            🛰️ DB-Scout
          </motion.h1>
          <p className="text-cyber-text-muted font-mono text-sm uppercase tracking-widest">
            by Team ZeroKelvin
          </p>
          <p className="mt-4 text-cyber-text text-lg max-w-xl mx-auto opacity-80">
            The Agentic Reconnaissance Layer for Enterprise Data.
          </p>
        </header>

        <AnimatePresence mode="wait">
          {!showSchemaSelection ? (
            <motion.div 
              key="connection-form"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="grid grid-cols-1 md:grid-cols-12 gap-8"
            >
              {/* DB Type Selection */}
              <div className="md:col-span-4 space-y-3">
                <h3 className="text-xs font-bold text-cyber-text-muted uppercase tracking-wider mb-4">Select Source</h3>
                {DB_TYPES.map((type) => (
                  <button
                    key={type.id}
                    disabled={!type.active}
                    onClick={() => setSelectedType(type.id)}
                    className={`w-full flex items-center justify-between p-4 rounded-xl border transition-all duration-200 ${
                      selectedType === type.id 
                        ? 'bg-cyber-accent-muted border-cyber-accent text-cyber-accent' 
                        : 'bg-cyber-gray border-cyber-border text-cyber-text-muted hover:border-cyber-text/30'
                    } ${!type.active && 'opacity-50 cursor-not-allowed grayscale'}`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xl">{type.icon}</span>
                      <span className="font-medium">{type.name}</span>
                    </div>
                    {!type.active && (
                      <span className="text-[10px] bg-cyber-border px-2 py-0.5 rounded text-cyber-text">SOON</span>
                    )}
                    {selectedType === type.id && <ChevronRight size={16} />}
                  </button>
                ))}
              </div>

              {/* Connection Form */}
              <div className="md:col-span-8 bg-cyber-gray border border-cyber-border rounded-2xl p-8 shadow-2xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyber-accent/30 to-transparent" />
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-cyber-text-muted uppercase flex items-center gap-2">
                      <Globe size={12} /> Host
                    </label>
                    <input 
                      type="text" 
                      value={formData.host}
                      onChange={(e) => setFormData({...formData, host: e.target.value})}
                      placeholder="db.example.com"
                      className="w-full bg-cyber-black border border-cyber-border rounded-lg px-4 py-2.5 focus:border-cyber-accent outline-none transition-colors font-mono text-sm"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-cyber-text-muted uppercase flex items-center gap-2">
                      <Server size={12} /> Port
                    </label>
                    <input 
                      type="text" 
                      value={formData.port}
                      onChange={(e) => setFormData({...formData, port: e.target.value})}
                      placeholder="5432"
                      className="w-full bg-cyber-black border border-cyber-border rounded-lg px-4 py-2.5 focus:border-cyber-accent outline-none transition-colors font-mono text-sm"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-cyber-text-muted uppercase flex items-center gap-2">
                      <User size={12} /> Username
                    </label>
                    <input 
                      type="text" 
                      value={formData.user}
                      onChange={(e) => setFormData({...formData, user: e.target.value})}
                      placeholder="postgres"
                      className="w-full bg-cyber-black border border-cyber-border rounded-lg px-4 py-2.5 focus:border-cyber-accent outline-none transition-colors font-mono text-sm"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-cyber-text-muted uppercase flex items-center gap-2">
                      <Lock size={12} /> Password
                    </label>
                    <input 
                      type="password" 
                      value={formData.password}
                      onChange={(e) => setFormData({...formData, password: e.target.value})}
                      placeholder="••••••••"
                      className="w-full bg-cyber-black border border-cyber-border rounded-lg px-4 py-2.5 focus:border-cyber-accent outline-none transition-colors font-mono text-sm"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-cyber-text-muted uppercase flex items-center gap-2">
                      <Database size={12} /> Database
                    </label>
                    <input 
                      type="text" 
                      value={formData.database}
                      onChange={(e) => setFormData({...formData, database: e.target.value})}
                      placeholder="production_db"
                      className="w-full bg-cyber-black border border-cyber-border rounded-lg px-4 py-2.5 focus:border-cyber-accent outline-none transition-colors font-mono text-sm"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-cyber-text-muted uppercase flex items-center gap-2">
                      <ChevronRight size={12} /> Default Schema
                    </label>
                    <input 
                      type="text" 
                      value={formData.schema}
                      onChange={(e) => setFormData({...formData, schema: e.target.value})}
                      placeholder="public"
                      className="w-full bg-cyber-black border border-cyber-border rounded-lg px-4 py-2.5 focus:border-cyber-accent outline-none transition-colors font-mono text-sm"
                    />
                  </div>
                </div>

                <div className="mt-8 flex flex-col sm:flex-row gap-4">
                  <button
                    onClick={handleTestConnection}
                    disabled={testStatus === 'testing'}
                    className={`flex-1 flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${
                      testStatus === 'success' 
                        ? 'bg-green-500/10 text-green-500 border border-green-500/50' 
                        : 'bg-cyber-border text-cyber-text hover:bg-cyber-border/80 border border-transparent'
                    }`}
                  >
                    {testStatus === 'testing' ? (
                      <Loader2 size={18} className="animate-spin" />
                    ) : testStatus === 'success' ? (
                      <CheckCircle2 size={18} />
                    ) : (
                      <Database size={18} />
                    )}
                    {fetchingSchemas ? 'Fetching Schemas...' : 'Test Connection'}
                  </button>
                </div>

                <AnimatePresence>
                  {testStatus === 'error' && (
                    <motion.div 
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-3 text-red-500 text-sm"
                    >
                      <AlertCircle size={16} />
                      {errorMessage}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="schema-selection"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="max-w-2xl mx-auto bg-cyber-gray border border-cyber-border rounded-2xl p-8 shadow-2xl"
            >
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h3 className="text-xl font-bold text-cyber-accent">Schema Reconnaissance</h3>
                  <p className="text-sm text-cyber-text-muted">Select the target schemas for agentic analysis.</p>
                </div>
                <button 
                  onClick={() => setShowSchemaSelection(false)}
                  className="text-xs font-bold text-cyber-text-muted hover:text-cyber-text uppercase tracking-widest"
                >
                  Back to Config
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-8">
                {availableSchemas.map((schema) => (
                  <button
                    key={schema}
                    onClick={() => toggleSchema(schema)}
                    className={`flex items-center justify-between p-4 rounded-xl border transition-all ${
                      selectedSchemaList.includes(schema)
                        ? 'bg-cyber-accent-muted border-cyber-accent text-cyber-accent'
                        : 'bg-cyber-black border-cyber-border text-cyber-text-muted hover:border-cyber-text/30'
                    }`}
                  >
                    <span className="font-mono text-sm">{schema}</span>
                    {selectedSchemaList.includes(schema) && <CheckCircle2 size={16} />}
                  </button>
                ))}
              </div>

              <button
                onClick={handleDeploy}
                disabled={selectedSchemaList.length === 0}
                className={`w-full flex items-center justify-center gap-2 px-6 py-4 rounded-xl font-bold transition-all ${
                  selectedSchemaList.length > 0
                    ? 'bg-cyber-accent text-cyber-black hover:shadow-[0_0_20px_rgba(0,255,157,0.4)]'
                    : 'bg-cyber-border text-cyber-text-muted cursor-not-allowed'
                }`}
              >
                Deploy Scout Agent to {selectedSchemaList.length} Schema{selectedSchemaList.length > 1 ? 's' : ''}
                <ChevronRight size={18} />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
