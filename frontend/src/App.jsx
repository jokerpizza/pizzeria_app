import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [ingredients, setIngredients] = useState([])
  const [name, setName] = useState('')
  const [baseQuantity, setBaseQuantity] = useState('')
  const [unit, setUnit] = useState('g')
  const [priceForBase, setPriceForBase] = useState('')

  useEffect(() => {
    axios.get('/api/ingredients').then(res => setIngredients(res.data))
  }, [])

  const addIngredient = async () => {
    await axios.post('/api/ingredients', {
      name,
      base_quantity: parseFloat(baseQuantity),
      unit,
      price_for_base: parseFloat(priceForBase)
    })
    const res = await axios.get('/api/ingredients')
    setIngredients(res.data)
    setName('')
    setBaseQuantity('')
    setPriceForBase('')
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Składniki</h1>
      <div className="flex gap-2 mb-4">
        <input
          placeholder="Nazwa"
          value={name}
          onChange={e => setName(e.target.value)}
          className="border p-1"
        />
        <input
          placeholder="Ilość"
          type="number"
          value={baseQuantity}
          onChange={e => setBaseQuantity(e.target.value)}
          className="border p-1"
        />
        <select
          value={unit}
          onChange={e => setUnit(e.target.value)}
          className="border p-1"
        >
          <option value="g">g</option>
          <option value="kg">kg</option>
          <option value="ml">ml</option>
          <option value="l">l</option>
          <option value="szt">szt</option>
        </select>
        <input
          placeholder="Cena za tę ilość"
          type="number"
          value={priceForBase}
          onChange={e => setPriceForBase(e.target.value)}
          className="border p-1"
        />
        <button
          onClick={addIngredient}
          className="bg-green-600 text-white px-3"
        >
          Dodaj
        </button>
      </div>

      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="px-4 py-2">Nazwa</th>
            <th className="px-4 py-2">Ilość</th>
            <th className="px-4 py-2">Jednostka</th>
            <th className="px-4 py-2">Cena za ilość</th>
            <th className="px-4 py-2">Cena za 1 jednostkę</th>
          </tr>
        </thead>
        <tbody>
          {ingredients.map(i => (
            <tr key={i.id}>
              <td className="border px-4 py-2">{i.name}</td>
              <td className="border px-4 py-2">{i.base_quantity}</td>
              <td className="border px-4 py-2">{i.unit}</td>
              <td className="border px-4 py-2">{i.price_for_base.toFixed(2)} zł</td>
              <td className="border px-4 py-2">{i.price_per_unit.toFixed(2)} zł</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
)
}

export default App