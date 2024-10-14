import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { API_URL, MARKET_DATA_ENDPOINT } from '../constants/api';

const fetchCryptoData = async (symbol) => {
  const response = await fetch(`${API_URL}${MARKET_DATA_ENDPOINT}?symbol=${symbol}`);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

const CryptoChart = ({ symbol }) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ['cryptoData', symbol],
    queryFn: () => fetchCryptoData(symbol),
    refetchInterval: 60000, // Refetch every minute
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  // Transform data for the chart
  const chartData = data.map(item => ({
    time: new Date(item[0]).toLocaleTimeString(),
    price: parseFloat(item[4]),
  }));

  return (
    <div className="h-64 w-full">
      <h3 className="text-lg font-semibold mb-2">{symbol}</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <XAxis dataKey="time" />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip />
          <Line type="monotone" dataKey="price" stroke="#8884d8" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CryptoChart;