import React, { useEffect, useState } from 'react';
import { api } from '../api/client';

type Balance = { card: number; cash: number };

export default function CashBalance() {
  const [b, setB] = useState<Balance | null>(null);

  useEffect(() => {
    api.get<Balance>('/cash/balance').then(r => setB(r.data));
  }, []);

  if (!b) return <p>Ładowanie…</p>;
  return (
    <div style={{ background: 'white', borderRadius: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', padding: 16 }}>
      <h2 style={{ marginBottom: 8 }}>Saldo gotówkowe</h2>
      <table style={{ width: '100%', fontSize: 14 }}>
        <tbody>
          <tr><td>Stan początkowy</td><td style={{ textAlign: 'right' }}>0,00 zł</td></tr>
          <tr><td>Karta płatnicza</td><td style={{ textAlign: 'right' }}>{b.card.toFixed(2)} zł</td></tr>
          <tr><td>Gotówka</td><td style={{ textAlign: 'right' }}>{b.cash.toFixed(2)} zł</td></tr>
          <tr style={{ fontWeight: 'bold' }}><td>Łącznie</td><td style={{ textAlign: 'right' }}>{(b.card + b.cash).toFixed(2)} zł</td></tr>
        </tbody>
      </table>
    </div>
  );
}