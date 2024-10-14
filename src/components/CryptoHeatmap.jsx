import React from 'react';
import CryptoChart from './CryptoChart';

const CryptoHeatmap = () => {
  const symbols = ['BTCUSDT', 'ETHUSDT', 'GMTUSDT', 'FTMUSDT', 'ALGOUSDT', 'LUNAUSDT', 'DOGEUSDT'];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {symbols.map(symbol => (
        <CryptoChart key={symbol} symbol={symbol} />
      ))}
    </div>
  );
};

export default CryptoHeatmap;