import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function IngredientList() {
  const [ingredients, setIngredients] = useState([]);
  const [name, setName] = useState('');
  const [unit, setUnit] = useState('g');
  const [price, setPrice] = useState('');

  const api = import.meta.env.VITE_API_URL;

  useEffect(() => {
    axios.get(`${api}/ingredients`)
      .then(res => setIngredients(res.data))
      .catch(console.error);
  }, []);

  const addIngredient = () => {
    axios.post(`${api}/ingredients`, {
      name, unit, price_per_unit: parseFloat(price)
    }).then(res => {
      setIngredients(prev => [...prev, { id: res.data.id, name, unit, price_per_unit: parseFloat(price) }]);
      setName(''); setPrice('');
    }).catch(console.error);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Składniki</h1>
      <div className="flex space-x-2 mb-4">
        <input className="border p-2 flex-1" placeholder="Nazwa" value={name} onChange={e => setName(e.target.value)} />
        <select className="border p-2" value={unit} onChange={e => setUnit(e.target.value)}>
          <option value="g">g</option>
          <option value="kg">kg</option>
          <option value="ml">ml</option>
          <option value="l">l</option>
          <option value="szt">szt</option>
        </select>
        <input className="border p-2" placeholder="Cena" value={price} onChange={e => setPrice(e.target.value)} />
        <button className="bg-green-500 text-white px-4" onClick={addIngredient}>Dodaj</button>
      </div>
      <table className="w-full bg-white shadow rounded">
        <thead><tr><th className="p-2">Nazwa</th><th>Jedn.</th><th>Cena</th></tr></thead>
        <tbody>
          {ingredients.map(i => (
            <tr key={i.id} className="border-t">
              <td className="p-2">{i.name}</td>
              <td className="p-2">{i.unit}</td>
              <td className="p-2">{i.price_per_unit.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
      </table>
    </div>
  );
}
