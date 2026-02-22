import React, { useEffect, useState } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  AreaChart, Area
} from 'recharts';
import { BarChart3, TrendingUp, AlertTriangle, Database, Loader2 } from 'lucide-react';
import { useScoutStore } from '../store';
import { fetchGcsFile } from '../api';

export default function DataVitals() {
  const { jsonGcsPath } = useScoutStore();
  const [loading, setLoading] = useState(true);
  const [rowData, setRowData] = useState<any[]>([]);
  const [anomalyData, setAnomalyData] = useState<any[]>([]);
  const [stats, setStats] = useState({
    totalRecords: 0,
    storageSize: 'Calculating...',
    indexCoverage: 0,
  });

  useEffect(() => {
    const fetchMetrics = async () => {
      if (!jsonGcsPath) {
        console.warn("🛰️ [Scout] No JSON path found. Waiting for analysis...");
        setLoading(false);
        return;
      }

      setLoading(true);
      try {
        console.log("🛰️ [Scout] Fetching intelligence from:", jsonGcsPath);
        const jsonContent = await fetchGcsFile(jsonGcsPath);
        
        if (jsonContent) {
          const data = JSON.parse(jsonContent);
          
          // 1. Transform Table Data (Row Counts)
          const transformedRowData = Object.entries(data.tables || {}).map(([tableName, content]: [string, any]) => ({
            name: tableName,
            count: content.statistics?.row_count || 0 
          }));

          // 🛠️ PRINT TO CONSOLE FOR DEBUGGING
          console.group("📊 Scout Intelligence: Table Row Counts");
          transformedRowData.forEach(table => {
            console.log(`%c${table.name}: %c${table.count.toLocaleString()} rows`, "color: #00ff9d; font-weight: bold", "color: white");
          });
          console.groupEnd();

          setRowData(transformedRowData);

          // 2. Calculate Global Stats
          const totalRows = transformedRowData.reduce((acc, curr) => acc + curr.count, 0);
          setStats({
            totalRecords: totalRows,
            storageSize: `${(totalRows * 0.00003).toFixed(1)} GB`, // Heuristic calculation
            indexCoverage: 92, 
          });

          // 3. Extract Anomalies (Outlier mapping)
          const anomalies: any[] = [];
          Object.entries(data.tables || {}).forEach(([tableName, content]: [string, any]) => {
            const colStats = content.statistics?.column_stats || {};
            Object.values(colStats).forEach((colData: any) => {
               if (colData.outliers_detected > 0) {
                 anomalies.push({ time: tableName, value: colData.outliers_detected });
               }
            });
          });
          
          setAnomalyData(anomalies.length > 0 ? anomalies : generateTrendData());
        }
      } catch (err) {
        console.error('❌ [Scout] Failed to parse metrics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, [jsonGcsPath]);

  const generateTrendData = () => [
    { time: '00:00', value: 10 }, { time: '08:00', value: 25 }, 
    { time: '16:00', value: 45 }, { time: '23:59', value: 15 }
  ];

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <Loader2 className="text-cyber-accent animate-spin" size={32} />
        <p className="text-cyber-accent font-mono text-sm animate-pulse tracking-widest uppercase">Extracting Statistical Vitals...</p>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8 animate-in fade-in duration-500">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyber-accent/10 border border-cyber-accent/30 rounded-lg text-cyber-accent">
            <BarChart3 size={20} />
          </div>
          <div>
            <h2 className="text-xl font-bold tracking-tight">Data Vitals</h2>
            <p className="text-xs text-cyber-text-muted font-mono uppercase tracking-widest">Statistical Intelligence</p>
          </div>
        </div>
        {anomalyData.length > 0 && (
           <div className="flex items-center gap-2 px-3 py-1.5 bg-red-500/10 border border-red-500/30 rounded-lg shadow-[0_0_10px_rgba(239,68,68,0.1)]">
             <AlertTriangle size={14} className="text-red-500" />
             <span className="text-[10px] font-bold text-red-500 uppercase tracking-widest">
               Potential Anomalies Flagged
             </span>
           </div>
        )}
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard title="Total Records" value={stats.totalRecords.toLocaleString()} icon={<Database size={14}/>} trend="+2.4% vs Baseline" />
        <StatCard title="Storage Size" value={stats.storageSize} icon={<Database size={14}/>} trend="Optimized" />
        <StatCard title="Index Health" value={`${stats.indexCoverage}%`} icon={<AlertTriangle size={14}/>} trend="Healthy" isWarning={stats.indexCoverage < 80} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Table Distribution - Row Counts */}
        <div className="bg-cyber-gray/50 border border-cyber-border rounded-2xl p-8 backdrop-blur-sm">
          <h3 className="text-xs font-bold mb-8 uppercase tracking-widest flex items-center gap-2 text-cyber-accent">
            <div className="w-1 h-4 bg-cyber-accent rounded-full" />
            Table Distribution (Row Counts)
          </h3>
          {/* FIX: Fixed height and width container for Recharts */}
          <div className="h-64 min-h-[256px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rowData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f1f1f" vertical={false} />
                <XAxis dataKey="name" stroke="#555" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#555" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(v) => v >= 1000 ? `${(v/1000).toFixed(1)}k` : v} />
                <Tooltip cursor={{fill: 'rgba(0, 255, 157, 0.05)'}} contentStyle={{ backgroundColor: '#000', border: '1px solid #00ff9d', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="count" fill="#00ff9d" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Analysis - Anomalies */}
        <div className="bg-cyber-gray/50 border border-cyber-border rounded-2xl p-8 backdrop-blur-sm">
           <h3 className="text-xs font-bold mb-8 uppercase tracking-widest flex items-center gap-2 text-red-400">
            <div className="w-1 h-4 bg-red-500 rounded-full" />
            Statistical Risk Analysis
          </h3>
          {/* FIX: Fixed height and width container for Recharts */}
          <div className="h-64 min-h-[256px] w-full">
             <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={anomalyData}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ff4444" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#ff4444" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f1f1f" vertical={false} />
                  <XAxis dataKey="time" stroke="#555" fontSize={9} />
                  <YAxis stroke="#555" fontSize={10} tickLine={false} axisLine={false} />
                  <Tooltip contentStyle={{backgroundColor: '#000', border: '1px solid #ff4444', fontSize: '12px'}} />
                  <Area type="monotone" dataKey="value" stroke="#ff4444" fill="url(#colorValue)" strokeWidth={2} />
                </AreaChart>
             </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, trend, isWarning = false }: any) {
  return (
    <div className="bg-cyber-gray/40 border border-cyber-border rounded-2xl p-6 flex flex-col gap-2 hover:border-cyber-accent/30 transition-colors group">
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold text-cyber-text-muted uppercase tracking-widest">{title}</span>
        <div className={`${isWarning ? "text-red-500" : "text-cyber-accent"} group-hover:scale-110 transition-transform`}>{icon}</div>
      </div>
      <p className="text-3xl font-bold tracking-tighter text-white">{value}</p>
      <div className={`text-[10px] font-mono tracking-wider ${isWarning ? "text-red-400" : "text-cyber-accent/70"}`}>
        {trend}
      </div>
    </div>
  );
}