import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Recipes from './pages/Recipes';

const Layout: React.FC<{children: React.ReactNode}> = ({children}) => (
  <div style={{display:'flex', minHeight:'100vh'}}>
    <aside style={{width:220, background:'#f4f4f4', padding:'1rem'}}>
      <h2 style={{marginBottom:'1rem'}}>FoodCost</h2>
      <nav style={{display:'flex', flexDirection:'column', gap:'0.5rem'}}>
        <Link to="/">Dashboard</Link>
        <Link to="/products">Produkty</Link>
        <Link to="/recipes">Receptury</Link>
      </nav>
    </aside>
    <main style={{flex:1, padding:'1rem'}}>{children}</main>
  </div>
);

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Layout><Dashboard/></Layout>} />
      <Route path="/products" element={<Layout><Products/></Layout>} />
      <Route path="/recipes" element={<Layout><Recipes/></Layout>} />
    </Routes>
  </BrowserRouter>
);

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
