import React, { useEffect, useState } from 'react';
import { api } from '../api/client';

type Summary = { today: number; week: number; month: number; docsToday: number; docsWeek: number; docsMonth: number };

export default function SalesSummary() {
  const [s, setS] = useState<Summary | null>(null);

  useEffect(() => {
    api.get<Summary>('/sales/summary').then(r => setS(r.data));
  }, []);

  if (!s) return <p>Ładowanie…</p>;
  return (
    <div style={{ background: 'white', borderRadius: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', padding: 16 }}>
      <h2 style={{ marginBottom: 8 }}>Sprzedaż</h2>
      <table style={{ width: '100%', fontSize: 14 }}>
        <tbody>
          <tr>
            <td>Dziś</td>
            <td style={{ textAlign: 'right' }}>{s.today.toFixed(2)} zł</td>
            <td style={{ textAlign: 'right' }}>{s.docsToday}</td>
          </tr>
          <tr>
            <td>Ten tydzień</td>
            <td style={{ textAlign: 'right' }}>{s.week.toFixed(2)} zł</td>
            <td style={{ textAlign: 'right' }}>{s.docsWeek}</td>
          </tr>
          <tr>
            <td>Ten miesiąc</td>
            <td style={{ textAlign: 'right' }}>{s.month.toFixed(2)} zł</td>
            <td style={{ textAlign: 'right' }}>{s.docsMonth}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}