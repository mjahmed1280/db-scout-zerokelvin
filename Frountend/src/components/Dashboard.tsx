import React from 'react';
import { Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'motion/react';
import { 
  FileText, 
  MessageSquare, 
  Share2, 
  BarChart3, 
  Database, 
  Activity, 
  LogOut,
  ChevronRight,
  Search
} from 'lucide-react';
import { useScoutStore } from '../store';
import IntelligenceDocs from './IntelligenceDocs';
import ScoutChat from './ScoutChat';
import ERDMapper from './ERDMapper';
import DataVitals from './DataVitals';

export default function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();
  const { dbConfig, previewTables, reset } = useScoutStore();

  const handleLogout = () => {
    reset();
    navigate('/');
  };

  const navItems = [
    { path: '/dashboard', label: 'Intelligence Docs', icon: FileText },
    { path: '/dashboard/chat', label: 'Scout Chat', icon: MessageSquare },
    { path: '/dashboard/erd', label: 'ERD Mapper', icon: Share2 },
    { path: '/dashboard/vitals', label: 'Data Vitals', icon: BarChart3 },
  ];

  return (
    <div className="flex h-screen bg-cyber-black text-cyber-text overflow-hidden">
      {/* Sidebar */}
      <aside className="w-72 bg-cyber-gray border-r border-cyber-border flex flex-col">
        <div className="p-6 border-b border-cyber-border">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-cyber-accent rounded-lg flex items-center justify-center text-cyber-black font-bold text-xl">
              🛰️
            </div>
            <div>
              <h1 className="font-bold tracking-tighter text-lg leading-none">DB-Scout</h1>
              <span className="text-[10px] text-cyber-text-muted uppercase tracking-widest">v1.0.4 Recon</span>
            </div>
          </div>

          <div className="bg-cyber-black/50 rounded-xl p-4 border border-cyber-border">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-bold text-cyber-text-muted uppercase">Target DB</span>
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-cyber-accent animate-pulse" />
                <span className="text-[10px] font-bold text-cyber-accent uppercase">Live</span>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm font-mono truncate">
              <Database size={14} className="text-cyber-text-muted" />
              {dbConfig?.database || 'Unknown'}
            </div>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto p-4 space-y-1">
          <div className="px-2 mb-2">
            <span className="text-[10px] font-bold text-cyber-text-muted uppercase tracking-widest">Modules</span>
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || (item.path === '/dashboard' && location.pathname === '/dashboard/');
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                  isActive 
                    ? 'bg-cyber-accent-muted text-cyber-accent border border-cyber-accent/20' 
                    : 'text-cyber-text-muted hover:text-cyber-text hover:bg-cyber-border/30'
                }`}
              >
                <Icon size={18} className={isActive ? 'text-cyber-accent' : 'text-cyber-text-muted group-hover:text-cyber-text'} />
                <span className="text-sm font-medium">{item.label}</span>
                {isActive && (
                  <motion.div 
                    layoutId="active-nav"
                    className="ml-auto w-1 h-4 bg-cyber-accent rounded-full"
                  />
                )}
              </Link>
            );
          })}

          <div className="mt-8 px-2 mb-2">
            <span className="text-[10px] font-bold text-cyber-text-muted uppercase tracking-widest">Reconnaissance Overview</span>
          </div>
          <div className="space-y-1 px-2">
            {previewTables.map((table) => (
              <div key={table} className="flex items-center gap-2 py-1.5 group cursor-default">
                <div className="w-1 h-1 rounded-full bg-cyber-border group-hover:bg-cyber-accent transition-colors" />
                <span className="text-xs font-mono text-cyber-text-muted group-hover:text-cyber-text transition-colors">
                  {table}
                </span>
              </div>
            ))}
          </div>
        </nav>

        <div className="p-4 border-t border-cyber-border">
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-cyber-text-muted hover:text-red-400 hover:bg-red-400/10 transition-all duration-200"
          >
            <LogOut size={18} />
            <span className="text-sm font-medium">Terminate Session</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden flex flex-col">
        <header className="h-16 border-b border-cyber-border flex items-center justify-between px-8 bg-cyber-gray/30 backdrop-blur-md">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-cyber-text-muted">
              <Activity size={16} />
              <span className="text-xs font-mono uppercase tracking-widest">System Operational</span>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <div className="relative group">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-cyber-text-muted group-focus-within:text-cyber-accent transition-colors" size={14} />
              <input 
                type="text" 
                placeholder="Search intelligence..."
                className="bg-cyber-black border border-cyber-border rounded-full pl-9 pr-4 py-1.5 text-xs outline-none focus:border-cyber-accent transition-all w-64"
              />
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <p className="text-[10px] font-bold text-cyber-text uppercase leading-none">Local Dev</p>
                <p className="text-[9px] text-cyber-text-muted uppercase tracking-tighter">Security Level 4</p>
              </div>
              <div className="w-8 h-8 rounded-full bg-cyber-border border border-cyber-accent/20 flex items-center justify-center text-[10px] font-bold">
                LD
              </div>
            </div>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto bg-cyber-black relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full"
            >
              <Routes>
                <Route index element={<IntelligenceDocs />} />
                <Route path="chat" element={<ScoutChat />} />
                <Route path="erd" element={<ERDMapper />} />
                <Route path="vitals" element={<DataVitals />} />
              </Routes>
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
