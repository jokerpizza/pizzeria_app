import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import IngredientList from './components/IngredientList';
import RecipeList from './components/RecipeList';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 bg-gray-100 p-4 overflow-auto">
          <Routes>
            <Route path="/" element={<h1 className="text-2xl font-bold">Dashboard</h1>} />
            <Route path="/ingredients" element={<IngredientList />} />
            <Route path="/recipes" element={<RecipeList />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
