import React, { useEffect, useState, useRef } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import mermaid from 'mermaid';
import { motion } from 'framer-motion';
import { FileText, Download, Copy, Check, Loader2, AlertCircle } from 'lucide-react';
import { useScoutStore } from '../store';
import { fetchGcsFile } from '../api';

// Initialize Mermaid with Cyber Aesthetics
mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#00ff9d',
    primaryTextColor: '#fff',
    primaryBorderColor: '#00ff9d',
    lineColor: '#00ff9d',
    secondaryColor: '#121212',
    tertiaryColor: '#050505',
  },
  securityLevel: 'loose',
});

// Helper Component to render the Mermaid SVG
const MermaidRenderer = ({ chart }: { chart: string }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current && chart) {
      const renderDiagram = async () => {
        try {
          // Generate a unique ID for each diagram
          const id = `mermaid-${Math.random().toString(36).substr(2, 9)}`;
          const { svg } = await mermaid.render(id, chart);
          if (ref.current) {
            ref.current.innerHTML = svg;
          }
        } catch (error) {
          console.error("Mermaid rendering failed:", error);
          if (ref.current) ref.current.innerHTML = "<p className='text-red-500'>Failed to render diagram.</p>";
        }
      };
      renderDiagram();
    }
  }, [chart]);

  return (
    <div className="flex justify-center my-10 p-6 bg-cyber-black/50 border border-cyber-border rounded-2xl overflow-x-auto shadow-2xl group">
       <div ref={ref} className="transition-transform duration-500 group-hover:scale-[1.02]" />
    </div>
  );
};

export default function IntelligenceDocs() {
  const { mdGcsPath } = useScoutStore();
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchDocs = async () => {
      if (!mdGcsPath) {
        setContent('# 🛰️ Intelligence Report Pending\n\nDeploy the Scout Agent to scan the data graveyard.');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(false);

      try {
        const markdownContent = await fetchGcsFile(mdGcsPath);
        if (markdownContent) {
          setContent(markdownContent);
        } else {
          throw new Error("Empty content received");
        }
      } catch (err) {
        setError(true);
        setContent(`# ⚠️ Access Denied\n\n**Source:** \`${mdGcsPath}\`\n\nUnable to retrieve report.`);
      } finally {
        setLoading(false);
      }
    };

    fetchDocs();
  }, [mdGcsPath]);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-6">
        <Loader2 className="text-cyber-accent animate-spin" size={48} />
        <p className="text-cyber-accent font-mono text-sm tracking-widest uppercase animate-pulse">Decrypting Intel...</p>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-5xl mx-auto">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-cyber-accent/10 border border-cyber-accent/30 rounded-xl text-cyber-accent shadow-[0_0_15px_rgba(0,255,157,0.1)]">
            <FileText size={24} />
          </div>
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Intelligence Report</h2>
            <p className="text-[10px] text-cyber-text-muted font-mono uppercase tracking-widest truncate max-w-[300px]">
              {mdGcsPath}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={handleCopy}
            className="flex items-center gap-2 px-4 py-2 bg-cyber-gray border border-cyber-border rounded-lg text-xs font-bold hover:text-cyber-accent transition-all"
          >
            {copied ? <Check size={14} /> : <Copy size={14} />} {copied ? 'Copied' : 'Copy Source'}
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-cyber-accent text-cyber-black rounded-lg text-xs font-bold hover:shadow-[0_0_20px_rgba(0,255,157,0.4)] transition-all">
            <Download size={14} /> Export Intel
          </button>
        </div>
      </div>

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="relative">
        <div className="bg-cyber-gray/50 backdrop-blur-sm border border-cyber-border rounded-2xl p-8 md:p-12 shadow-2xl relative">
          
          {/* Apply the custom prose-cyber utility class */}
          <div className="prose-cyber prose-invert max-w-none">
            <Markdown 
              remarkPlugins={[remarkGfm]}
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  const codeValue = String(children).replace(/\n$/, '');
                  
                  // Check if this is a Mermaid diagram
                  if (!inline && (match?.[1] === 'mermaid' || codeValue.startsWith('erDiagram'))) {
                    return <MermaidRenderer chart={codeValue} />;
                  }
                  
                  return (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                }
              }}
            >
              {content}
            </Markdown>
          </div>
        </div>
      </motion.div>
    </div>
  );
}