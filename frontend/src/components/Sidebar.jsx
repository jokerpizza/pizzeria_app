import React from 'react'

export default function Sidebar() {
  return (
    <div className="w-64 bg-white border-r">
      <nav className="p-4 space-y-2">
        <a href="#" className="block px-2 py-1 hover:bg-green-100 rounded">Dashboard</a>
        <a href="#/ingredients" className="block px-2 py-1 hover:bg-green-100 rounded">Składniki</a>
        <a href="#/recipes" className="block px-2 py-1 hover:bg-green-100 rounded">Receptury</a>
        <a href="#/reports" className="block px-2 py-1 hover:bg-green-100 rounded">Raporty</a>
      </nav>
    </div>
  )
}
