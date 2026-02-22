import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Gateway from './Gateway';
import Scouting from './Scouting';
import Dashboard from './components/Dashboard';
import { useScoutStore } from './store';

export default function App() {
  const { isConnected, ragCorpusId } = useScoutStore();

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Gateway />} />
        <Route 
          path="/scouting" 
          element={isConnected ? <Scouting /> : <Navigate to="/" />} 
        />
        <Route 
          path="/dashboard/*" 
          element={ragCorpusId ? <Dashboard /> : <Navigate to="/" />} 
        />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}
