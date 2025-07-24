import { useState, useEffect } from 'react'
import axios from 'axios'

export default function Ingredients() {
  const [ingredients, setIngredients] = useState([])
  const [form, setForm] = useState({ name: '', base_quantity: '', unit: 'g', price_for_base: '' })

  useEffect(() => {
    axios.get('/api/ingredients').then(res => setIngredients(res.data))
  }, [])

  const handleAdd = async () => {
    await axios.post('/api/ingredients', form)
    const res = await axios.get('/api/ingredients')
    setIngredients(res.data)
    setForm({ name: '', base_quantity: '', unit: 'g', price_for_base: '' })
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Składniki</h1>
      <div className="flex mb-4 space-x-2">
        <input className="border p-2 rounded flex-1" placeholder="Nazwa" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
        <input className="border p-2 w-24 rounded" placeholder="Ilość" type="number" value={form.base_quantity} onChange={e => setForm({ ...form, base_quantity: e.target.value })} />
        <select className="border p-2 rounded" value={form.unit} onChange={e => setForm({ ...form, unit: e.target.value })}>
          <option>g</option><option>kg</option><option>ml</option><option>l</option><option>szt</option>
        </select>
        <input className="border p-2 w-32 rounded" placeholder="Cena za ilość" type="number" value={form.price_for_base} onChange={e => setForm({ ...form, price_for_base: e.target.value })} />
        <button onClick={handleAdd} className="bg-green-600 text-white px-4 rounded">Dodaj</button>
      </div>
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-4 py-2">Nazwa</th><th className="px-4 py-2">Ilość</th>
            <th className="px-4 py-2">Jednostka</th><th className="px-4 py-2">Cena za ilość</th>
            <th className="px-4 py-2">Cena za 1 jednostkę</th>
          </tr>
        </thead>
        <tbody>
          {ingredients.map(i => (
            <tr key={i.id} className="border-t">
              <td className="px-4 py-2">{i.name}</td>
              <td className="px-4 py-2">{i.base_quantity}</td>
              <td className="px-4 py-2">{i.unit}</td>
              <td className="px-4 py-2">{i.price_for_base.toFixed(2)} zł</td>
              <td className="px-4 py-2">{i.price_per_unit.toFixed(2)} zł</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
) }