import React, { useEffect, useState } from 'react';
import { ComposedChart, Line, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { api } from '../api/client';

type DataPoint = { day: string; current: number; previous: number };

export default function SalesChart() {
  const [data, setData] = useState<DataPoint[]>([]);

  useEffect(() => {
    api.get<DataPoint[]>('/sales/daily').then(res => setData(res.data));
  }, []);

  return (
    <div style={{ background: 'white', borderRadius: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', padding: 16 }}>
      <h2 style={{ marginBottom: 8 }}>Dzienne utargi</h2>
      <ResponsiveContainer width="100%" height={250}>
        <ComposedChart data={data}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend verticalAlign="top" />
          <Bar dataKey="current" name="Wybrany okres" barSize={20} />
          <Line type="monotone" dataKey="previous" name="Poprzedni okres" stroke="#3b82f6" strokeWidth={2}/>
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}