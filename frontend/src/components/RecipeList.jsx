import React, { useState, useEffect } from 'react'
import axios from 'axios'
import RecipeModal from './RecipeModal'

export default function RecipeList() {
  const [recipes, setRecipes] = useState([])
  const [showModal, setShowModal] = useState(false)
  const api = import.meta.env.VITE_API_URL

  const fetchRecipes = async () => {
    try {
      const res = await axios.get(`${api}/recipes`)
      setRecipes(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    fetchRecipes()
  }, [])

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Receptury</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          Dodaj recepturę
        </button>
      </div>

      <RecipeModal
        visible={showModal}
        onClose={() => setShowModal(false)}
        onSaved={fetchRecipes}
      />

      <table className="w-full bg-white shadow rounded">
        <thead>
          <tr>
            <th className="p-2">Nazwa</th>
            <th className="p-2">Kategoria</th>
            <th className="p-2">FC %</th>
            <th className="p-2">Marża %</th>
            <th className="p-2">Narzut %</th>
            <th className="p-2">Zysk PLN</th>
          </tr>
        </thead>
        <tbody>
          {(Array.isArray(recipes) ? recipes : []).map(r => (
            <tr key={r.id} className="border-t">
              <td className="p-2">{r.name}</td>
              <td className="p-2">{r.category}</td>
              <td className="p-2">{r.food_cost_dine_in.toFixed(1)}</td>
              <td className="p-2">{r.margin_dine_in.toFixed(1)}</td>
              <td className="p-2">{r.markup_dine_in.toFixed(1)}</td>
              <td className="p-2">{r.profit_pln_dine_in.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
)
}
