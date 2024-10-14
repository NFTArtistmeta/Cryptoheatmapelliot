import React from 'react';
import CryptoHeatmap from '../components/CryptoHeatmap';

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-4xl font-bold mb-8 text-center">Crypto Multi-Chart Dashboard</h1>
      <CryptoHeatmap />
    </div>
  );
};

export default Index;