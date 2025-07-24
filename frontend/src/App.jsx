import React from 'react'
import Sidebar from './components/Sidebar'

export default function App() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 bg-gray-100 p-4">
        <h1 className="text-2xl font-bold">Dashboard</h1>
      </div>
    </div>
  )
}
