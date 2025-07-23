import React from 'react'
import { BrowserRouter,Routes,Route,Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import MappingPage from './pages/Mapping'

export default function AppRoutes(){
  return <BrowserRouter>
    <nav style={{padding:10}}>
      <Link to="/">Dashboard</Link> | <Link to="/mapowanie">Mapowanie</Link>
    </nav>
    <Routes>
      <Route path="/" element={<Dashboard/>}/>
      <Route path="/mapowanie" element={<MappingPage/>}/>
    </Routes>
  </BrowserRouter>
}
