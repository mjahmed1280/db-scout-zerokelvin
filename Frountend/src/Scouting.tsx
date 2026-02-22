import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Loader2, Terminal, Shield, Search, Database, Cpu } from 'lucide-react';
import { useScoutStore } from './store';
import { useNavigate } from 'react-router-dom';
import { runAnalysis } from './api';

const STEPS = [
  { id: 1, text: "Establishing Secure MCP Connection...", icon: Shield },
  { id: 2, text: "Scouting Schema & Extracting Metadata...", icon: Search },
  { id: 3, text: "Generating Agentic Knowledge Base...", icon: Database },
  { id: 4, text: "Indexing Vectors in Vertex AI...", icon: Cpu },
];

export default function Scouting() {
  const navigate = useNavigate();
  const { dbConfig, selectedSchemas, setAnalysisResults } = useScoutStore();
  const [currentStep, setCurrentStep] = useState(0);
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    const runScout = async () => {
      try {
        // Animate steps while waiting for API response
        for (let i = 0; i < STEPS.length; i++) {
          setCurrentStep(i);
          setLogs(prev => [...prev, `> ${STEPS[i].text}`]);
          await new Promise(r => setTimeout(r, 1000));
        }

        // Call real API
        const data = await runAnalysis({ 
          user_id: "enterp user", 
          schema_name: selectedSchemas
        });

        if (data && data.status === 'success') {
          setAnalysisResults(data);
          setLogs(prev => [...prev, "> Analysis complete. Finalizing context..."]);
          await new Promise(r => setTimeout(r, 1000));
          navigate('/dashboard');
        } else {
          setLogs(prev => [...prev, `! Error: Analysis failed on backend`]);
        }
      } catch (err) {
        setLogs(prev => [...prev, "! Error: Network failure during scouting"]);
      }
    };

    runScout();
  }, [dbConfig, selectedSchemas, setAnalysisResults, navigate]);

  return (
    <div className="min-h-screen bg-cyber-black flex flex-col items-center justify-center p-6 font-mono">
      <div className="max-w-2xl w-full">
        <div className="mb-12 text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            className="inline-block mb-6"
          >
            <div className="w-20 h-20 rounded-full border-4 border-cyber-accent border-t-transparent flex items-center justify-center">
              <div className="w-12 h-12 rounded-full border-4 border-cyber-accent/30 border-b-transparent animate-spin" />
            </div>
          </motion.div>
          <h2 className="text-2xl font-bold text-cyber-accent tracking-tighter">AGENTIC SCOUT DEPLOYED</h2>
          <p className="text-cyber-text-muted mt-2">Analyzing data graveyard: {dbConfig?.database}</p>
        </div>

        <div className="bg-cyber-gray border border-cyber-border rounded-xl overflow-hidden shadow-2xl">
          <div className="bg-cyber-border/50 px-4 py-2 flex items-center gap-2 border-bottom border-cyber-border">
            <Terminal size={14} className="text-cyber-accent" />
            <span className="text-[10px] font-bold text-cyber-text-muted uppercase tracking-widest">Scout Terminal v1.0.4</span>
          </div>
          
          <div className="p-6 space-y-6">
            <div className="space-y-4">
              {STEPS.map((step, idx) => {
                const Icon = step.icon;
                const isActive = currentStep === idx;
                const isCompleted = currentStep > idx;

                return (
                  <div key={step.id} className={`flex items-center gap-4 transition-opacity duration-500 ${isActive ? 'opacity-100' : isCompleted ? 'opacity-60' : 'opacity-20'}`}>
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center border ${
                      isActive ? 'bg-cyber-accent-muted border-cyber-accent text-cyber-accent' : 
                      isCompleted ? 'bg-cyber-border border-cyber-border text-cyber-accent' : 
                      'bg-cyber-gray border-cyber-border text-cyber-text-muted'
                    }`}>
                      {isActive ? <Loader2 size={16} className="animate-spin" /> : <Icon size={16} />}
                    </div>
                    <span className={`text-sm ${isActive ? 'text-cyber-text font-bold' : 'text-cyber-text-muted'}`}>
                      {step.text}
                    </span>
                  </div>
                );
              })}
            </div>

            <div className="mt-8 pt-6 border-t border-cyber-border">
              <div className="h-32 overflow-y-auto space-y-1 text-[11px] text-cyber-accent/70 scrollbar-hide">
                <AnimatePresence mode="popLayout">
                  {logs.map((log, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="flex gap-2"
                    >
                      <span className="opacity-50">[{new Date().toLocaleTimeString()}]</span>
                      {log}
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 flex items-center justify-center gap-4 text-[10px] text-cyber-text-muted uppercase tracking-[0.2em]">
          <span className="flex items-center gap-1"><Shield size={10} /> Secure Tunnel</span>
          <span className="w-1 h-1 rounded-full bg-cyber-border" />
          <span className="flex items-center gap-1"><Cpu size={10} /> Vertex AI RAG</span>
          <span className="w-1 h-1 rounded-full bg-cyber-border" />
          <span className="flex items-center gap-1"><Database size={10} /> MCP Protocol</span>
        </div>
      </div>
    </div>
  );
}
