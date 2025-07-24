import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function RecipeList() {
  const [recipes, setRecipes] = useState([]);
  const api = import.meta.env.VITE_API_URL;

  useEffect(() => {
    axios.get(`${api}/recipes`)
      .then(res => setRecipes(res.data))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Receptury</h1>
      <table className="w-full bg-white shadow rounded">
        <thead><tr>
          <th className="p-2">Nazwa</th><th className="p-2">Kategoria</th>
          <th className="p-2">FC %</th><th className="p-2">Marża %</th>
          <th className="p-2">Narzut %</th><th className="p-2">Zysk PLN</th>
        </tr></thead>
        <tbody>
          {recipes.map(r => (
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
      </table>
    </div>
  );
}
