import React from 'react';

export default function FilterBar() {
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 16, background: 'white', borderRadius: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)', marginBottom: 16 }}>
      <div style={{ display: 'flex', gap: 8 }}>
        <select>
          <option>Wybierz kasę</option>
        </select>
        <select>
          <option>Bieżący tydzień</option>
        </select>
      </div>
      <button style={{ background: '#22c55e', color: 'white', border: 'none', borderRadius: 9999, padding: '8px 16px', cursor: 'pointer' }}>Szczegóły</button>
    </div>
  );
}