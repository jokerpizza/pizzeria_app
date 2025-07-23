import React, { useState } from 'react';
import IngredientsPage from './IngredientsPage';
import RecipesPage from './RecipesPage';
import Dashboard from './Dashboard';

export default function App() {
  const [tab, setTab] = useState('dashboard');
  return (
    <div>
      <nav>
        <button onClick={() => setTab('dashboard')}>Dashboard</button>
        <button onClick={() => setTab('ingredients')}>Składniki</button>
        <button onClick={() => setTab('recipes')}>Receptury</button>
      </nav>
      {tab === 'dashboard' && <Dashboard />}
      {tab === 'ingredients' && <IngredientsPage />}
      {tab === 'recipes' && <RecipesPage />}
    </div>
  );
}