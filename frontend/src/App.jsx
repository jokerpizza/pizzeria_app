import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Ingredients from './pages/Ingredients'
import Recipes from './pages/Recipes'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard/>}/>
        <Route path="ingredients" element={<Ingredients/>}/>
        <Route path="recipes" element={<Recipes/>}/>
      </Routes>
    </Layout>
  )
}
export default App