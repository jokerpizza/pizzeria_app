import React, { useEffect, useState } from 'react';
import { api } from '../api/client';

type Doc = { id: number; created_at: string; register: string; number: string };

export default function RecentDocuments() {
  const [docs, setDocs] = useState<Doc[] | null>(null);

  useEffect(() => {
    api.get<Doc[]>('/documents/recent').then(r => setDocs(r.data));
  }, []);

  if (!docs) return <p>Ładowanie…</p>;
  return (
    <div style={{ background: 'white', borderRadius: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', padding: 16 }}>
      <h2 style={{ marginBottom: 8 }}>Ostatnie dokumenty</h2>
      {docs.length === 0 ? <p>Brak dokumentów</p> : (
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {docs.map(d => (
            <li key={d.id} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
              <span>{new Date(d.created_at).toLocaleTimeString()}</span>
              <span>{d.register}</span>
              <a href="#">{d.number}</a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}