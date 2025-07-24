import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Recipes() {
  const [recipes, setRecipes] = useState([])

  useEffect(() => {
    axios.get('/api/recipes').then(res => setRecipes(res.data))
  }, [])

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Receptury</h1>
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-4 py-2">Nazwa</th><th className="px-4 py-2">Kategoria</th>
            <th className="px-4 py-2">FoodCost %</th><th className="px-4 py-2">Marża PLN</th>
          </tr>
        </thead>
        <tbody>
          {recipes.map(r => (
            <tr key={r.id} className="border-t">
              <td className="px-4 py-2">{r.name}</td>
              <td className="px-4 py-2">{r.category}</td>
              <td className="px-4 py-2">{r.food_cost_dine_in_pct.toFixed(1)}%</td>
              <td className="px-4 py-2">{r.margin_pln_dine.toFixed(2)} zł</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
}