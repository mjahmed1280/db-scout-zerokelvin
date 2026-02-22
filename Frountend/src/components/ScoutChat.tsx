import React, { useState, useRef, useEffect } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, User, Bot, Loader2, Sparkles, Terminal, Copy, Check } from 'lucide-react';
import { useScoutStore } from '../store';
import { sendChatMessage } from '../api';
import { v4 as uuidv4 } from 'uuid';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  text: string;
}

export default function ScoutChat() {
  const { ragCorpusId, sessionId, setSessionId } = useScoutStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!sessionId) setSessionId(uuidv4());
  }, [sessionId, setSessionId]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg: Message = { id: uuidv4(), role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const response = await sendChatMessage({
        query: input,
        rag_corpus_id: ragCorpusId || '',
        session_id: sessionId || ''
      });

      if (response?.response) {
        const botMsg: Message = { id: uuidv4(), role: 'assistant', text: response.response };
        setMessages(prev => [...prev, botMsg]);
      } else {
        throw new Error("Empty response");
      }
    } catch (err) {
      const errorMsg: Message = { 
        id: uuidv4(), 
        role: 'assistant', 
        text: "⚠️ **Connection Error:** Scout Agent is unreachable. Check your RAG pipeline status." 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-cyber-black">
      {/* Header */}
      <div className="px-8 py-4 border-b border-cyber-border bg-cyber-gray/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-cyber-accent/10 flex items-center justify-center text-cyber-accent border border-cyber-accent/30 shadow-[0_0_10px_rgba(0,255,157,0.2)]">
            <Sparkles size={16} />
          </div>
          <div>
            <h2 className="text-sm font-bold tracking-tight text-white">Scout Intelligence Chat</h2>
            <p className="text-[10px] text-cyber-text-muted font-mono uppercase">Session: {sessionId?.slice(0, 8)}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-cyber-accent/5 rounded-full border border-cyber-accent/20">
          <div className="w-1.5 h-1.5 rounded-full bg-cyber-accent animate-pulse" />
          <span className="text-[10px] font-bold text-cyber-accent uppercase tracking-widest">Agent Link Active</span>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-8 space-y-6 scrollbar-hide">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto space-y-6">
            <div className="p-6 bg-cyber-gray/40 border border-cyber-border rounded-2xl backdrop-blur-sm">
              <Terminal className="text-cyber-accent mx-auto mb-3" size={32} />
              <h3 className="text-sm font-bold mb-2 text-white">RAG CORPUS LOADED</h3>
              <p className="text-xs text-cyber-text-muted leading-relaxed">
                I have indexed your schema documentation. I can analyze relationships, explain column entropy, or generate SQL based on your database vitals.
              </p>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, x: msg.role === 'user' ? 20 : -20 }}
            animate={{ opacity: 1, x: 0 }}
            className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border ${
              msg.role === 'user' ? 'bg-cyber-gray border-cyber-border' : 'bg-cyber-accent/10 border-cyber-accent/40 text-cyber-accent'
            }`}>
              {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
            </div>
            <div className={`max-w-[85%] p-5 rounded-2xl relative group ${
              msg.role === 'user' 
                ? 'bg-cyber-accent/5 border border-cyber-accent/20 text-cyber-text' 
                : 'bg-cyber-gray/80 border border-cyber-border text-cyber-text shadow-xl'
            }`}>
              <div className="prose-cyber prose-invert max-w-none text-sm leading-relaxed">
                <Markdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code({node, inline, className, children, ...props}) {
                      return (
                        <code className="bg-black/40 px-1.5 py-0.5 rounded text-cyber-accent font-mono border border-cyber-border/50" {...props}>
                          {children}
                        </code>
                      )
                    }
                  }}
                >
                  {msg.text}
                </Markdown>
              </div>
              {msg.role === 'assistant' && (
                <button 
                  onClick={() => handleCopy(msg.id, msg.text)}
                  className="absolute top-2 right-2 p-1.5 opacity-0 group-hover:opacity-100 transition-opacity text-cyber-text-muted hover:text-cyber-accent"
                >
                  {copiedId === msg.id ? <Check size={14} /> : <Copy size={14} />}
                </button>
              )}
            </div>
          </motion.div>
        ))}

        {isTyping && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4">
            <div className="w-8 h-8 rounded-lg bg-cyber-accent/10 border border-cyber-accent/40 text-cyber-accent flex items-center justify-center">
              <Bot size={16} />
            </div>
            <div className="bg-cyber-gray border border-cyber-border p-4 rounded-2xl min-w-[240px]">
              <div className="flex items-center gap-2 mb-2">
                <Loader2 size={12} className="text-cyber-accent animate-spin" />
                <span className="text-[10px] font-mono text-cyber-accent uppercase tracking-widest animate-pulse">Scout Analyzing...</span>
              </div>
              <div className="h-1 w-full bg-cyber-border rounded-full overflow-hidden">
                <motion.div 
                  className="h-full bg-cyber-accent"
                  initial={{ width: "0%" }}
                  animate={{ width: "100%" }}
                  transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                />
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input */}
      <div className="p-8 border-t border-cyber-border bg-cyber-gray/10">
        <div className="max-w-4xl mx-auto relative">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Search Intelligence Database..."
            className="w-full bg-cyber-gray/50 border border-cyber-border rounded-2xl pl-6 pr-14 py-4 outline-none focus:border-cyber-accent focus:ring-1 focus:ring-cyber-accent/20 transition-all text-sm placeholder:text-cyber-text-muted shadow-2xl"
          />
          <button 
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className={`absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-xl flex items-center justify-center transition-all ${
              input.trim() && !isTyping 
                ? 'bg-cyber-accent text-cyber-black shadow-[0_0_15px_rgba(0,255,157,0.3)] hover:scale-105' 
                : 'bg-cyber-border text-cyber-text-muted cursor-not-allowed'
            }`}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}