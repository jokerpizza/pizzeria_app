import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Products from './pages/Products'
import Recipes from './pages/Recipes'
import Settings from './pages/Settings'

type Page = 'dashboard'|'products'|'recipes'|'settings'

export default function App(){
  const [page,setPage]=useState<Page>('dashboard')

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-brand text-white flex flex-col">
        <div className="p-4 text-2xl font-bold">FoodCost v2</div>
        <nav className="flex-1">
          <Btn p={page} set={setPage} val="dashboard">Dashboard</Btn>
          <Btn p={page} set={setPage} val="products">Produkty</Btn>
          <Btn p={page} set={setPage} val="recipes">Receptury</Btn>
          <Btn p={page} set={setPage} val="settings">Ustawienia</Btn>
        </nav>
        <div className="p-2 text-xs opacity-70">v0.2.0</div>
      </aside>
      <main className="flex-1 overflow-auto p-6">
        {page==='dashboard' && <Dashboard/>}
        {page==='products' && <Products/>}
        {page==='recipes' && <Recipes/>}
        {page==='settings' && <Settings/>}
      </main>
    </div>
  )
}

function Btn({p,set,val,children}:{p:Page,set:(p:Page)=>void,val:Page,children:any}){
  return <button className={"w-full text-left p-3 hover:bg-green-700 "+(p===val?'bg-green-800':'')} onClick={()=>set(val)}>{children}</button>
}
