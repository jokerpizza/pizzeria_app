import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Recipes from './pages/Recipes'

const App = () => (
  <BrowserRouter>
    <nav style={{display:'flex', gap:'1rem', padding:'1rem', borderBottom:'1px solid #ddd'}}>
      <Link to="/">Dashboard</Link>
      <Link to="/products">Products</Link>
      <Link to="/recipes">Recipes</Link>
    </nav>
    <div style={{padding:'1rem'}}>
      <Routes>
        <Route path="/" element={<Dashboard/>}/>
        <Route path="/products" element={<Products/>}/>
        <Route path="/recipes" element={<Recipes/>}/>
      </Routes>
    </div>
  </BrowserRouter>
)

ReactDOM.createRoot(document.getElementById('root')!).render(<App />)
