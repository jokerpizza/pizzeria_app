import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Products from "./pages/Products";
import Recipes from "./pages/Recipes";
import Categories from "./pages/Categories";

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex gap-4 p-4 bg-gray-200 mb-8">
        <Link to="/">Dashboard</Link>
        <Link to="/products">Produkty</Link>
        <Link to="/recipes">Przepisy</Link>
        <Link to="/categories">Kategorie</Link>
      </div>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/products" element={<Products />} />
        <Route path="/recipes" element={<Recipes />} />
        <Route path="/categories" element={<Categories />} />
      </Routes>
    </BrowserRouter>
  );
}