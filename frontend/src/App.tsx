
import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Recipes from './pages/Recipes'
import Sales from './pages/Sales'

type Page = 'dashboard'|'products'|'recipes'|'sales'

export default function App(){
  const [page, setPage] = useState<Page>('dashboard')

  const btnClasses = (active:boolean)=>"w-full text-left p-3 hover:bg-green-700 " + (active?"bg-green-800":"");

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-brand text-white flex flex-col">
        <div className="p-4 text-2xl font-bold">FoodCost</div>
        <nav className="flex-1 space-y-1">
          <button className={btnClasses(page==='dashboard')} onClick={()=>setPage('dashboard')}>Dashboard</button>
          <button className={btnClasses(page==='products')} onClick={()=>setPage('products')}>Produkty</button>
          <button className={btnClasses(page==='recipes')} onClick={()=>setPage('recipes')}>Receptury</button>
          <button className={btnClasses(page==='sales')} onClick={()=>setPage('sales')}>Sprzedaż</button>
        </nav>
        <div className="p-2 text-xs opacity-70">v0.2.0</div>
      </aside>
      <main className="flex-1 overflow-auto p-6">
        {page==='dashboard' && <Dashboard/>}
        {page==='products' && <Products/>}
        {page==='recipes' && <Recipes/>}
        {page==='sales' && <Sales/>}
      </main>
    </div>
  )
}
