import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { motion } from 'motion/react';
import { Share2, Maximize2, RefreshCw, Loader2, Info } from 'lucide-react';
import { useScoutStore } from '../store';
import { fetchGcsFile } from '../api';

mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  securityLevel: 'loose',
  themeVariables: {
    primaryColor: '#00ff9d',
    primaryTextColor: '#fff',
    primaryBorderColor: '#00ff9d',
    lineColor: '#00ff9d',
    secondaryColor: '#121212',
    tertiaryColor: '#1f1f1f',
  }
});

export default function ERDMapper() {
  const { jsonGcsPath } = useScoutStore();
  const [loading, setLoading] = useState(true);
  const [svg, setSvg] = useState('');
  const mermaidRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const renderChart = async () => {
      setLoading(true);

      if (!jsonGcsPath) {
        setLoading(false);
        return;
      }

      try {
        // Fetch real ER diagram data from GCS
        const jsonContent = await fetchGcsFile(jsonGcsPath);
        let definition = '';

        if (jsonContent) {
          try {
            const data = JSON.parse(jsonContent);
            // Transform JSON to Mermaid ER syntax
            // This assumes the JSON has a specific structure with entities and relationships
            definition = generateMermaidDefinition(data);
          } catch (e) {
            console.error('Failed to parse JSON:', e);
            // Fallback to a minimal diagram
            definition = getDefaultMermaidDefinition();
          }
        } else {
          definition = getDefaultMermaidDefinition();
        }

        const { svg } = await mermaid.render('mermaid-svg', definition);
        setSvg(svg);
      } catch (err) {
        console.error('Mermaid render failed:', err);
      } finally {
        setLoading(false);
      }
    };

    renderChart();
  }, [jsonGcsPath]);

  // Helper function to transform JSON to Mermaid ER syntax
  const generateMermaidDefinition = (data: any): string => {
    // This is a placeholder - adapt based on actual JSON structure from backend
    return getDefaultMermaidDefinition();
  };

  // Default Mermaid definition if API data unavailable
  const getDefaultMermaidDefinition = (): string => {
    return `
      erDiagram
        USERS ||--o{ ORDERS : places
        ORDERS ||--|{ ORDER_ITEMS : contains
        PRODUCTS ||--o{ ORDER_ITEMS : included_in
        PRODUCTS ||--|| INVENTORY : tracks
        ORDERS ||--o{ SHIPPING_LOGS : generates
        USERS ||--o{ AUTH_AUDIT : triggers
        
        USERS {
          string id PK
          string email
          string name
          timestamp created_at
        }
        ORDERS {
          string id PK
          string user_id FK
          float total_amount
          string status
        }
        PRODUCTS {
          string id PK
          string name
          float price
        }
    `;
  };

  return (
    <div className="h-full flex flex-col p-8">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyber-accent-muted rounded-lg text-cyber-accent">
            <Share2 size={20} />
          </div>
          <div>
            <h2 className="text-xl font-bold tracking-tight">ERD Mapper</h2>
            <p className="text-xs text-cyber-text-muted font-mono uppercase">Relational Reconnaissance</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button className="p-2 bg-cyber-gray border border-cyber-border rounded-lg text-cyber-text-muted hover:text-cyber-accent transition-colors">
            <RefreshCw size={18} />
          </button>
          <button className="p-2 bg-cyber-gray border border-cyber-border rounded-lg text-cyber-text-muted hover:text-cyber-accent transition-colors">
            <Maximize2 size={18} />
          </button>
        </div>
      </div>

      <div className="flex-1 bg-cyber-gray border border-cyber-border rounded-2xl relative overflow-hidden flex items-center justify-center p-8">
        {loading ? (
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="text-cyber-accent animate-spin" size={32} />
            <p className="text-cyber-text-muted font-mono text-sm animate-pulse">MAPPING RELATIONSHIPS...</p>
          </div>
        ) : (
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full h-full flex items-center justify-center"
            dangerouslySetInnerHTML={{ __html: svg }}
          />
        )}

        <div className="absolute bottom-6 right-6 flex items-center gap-2 px-3 py-1.5 bg-cyber-black/80 border border-cyber-border rounded-lg text-[10px] text-cyber-text-muted font-mono">
          <Info size={12} className="text-cyber-accent" />
          SCROLL TO ZOOM | DRAG TO PAN
        </div>
      </div>
    </div>
  );
}
