import React, { useEffect, useState } from 'react';
import { api } from '../api/client';

type Account = { id: number; name: string; balance: number };

export default function OpenAccounts() {
  const [acc, setAcc] = useState<Account[] | null>(null);

  useEffect(() => {
    api.get<Account[]>('/accounts/open').then(r => setAcc(r.data));
  }, []);

  return (
    <div style={{ background: 'white', borderRadius: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', padding: 16 }}>
      <h2 style={{ marginBottom: 8 }}>Otwarte rachunki</h2>
      {!acc ? <p>Ładowanie…</p> : acc.length === 0 ? <p>Nie są dostępne żadne dane</p> : (
        <ul>
          {acc.map(a => (
            <li key={a.id}>{a.name}: {a.balance.toFixed(2)}</li>
          ))}
        </ul>
      )}
    </div>
  );
}