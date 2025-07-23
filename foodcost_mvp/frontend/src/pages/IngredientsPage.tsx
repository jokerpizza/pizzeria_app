import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

export default function IngredientsPage() {
  const [ingredients, setIngredients] = useState([]);
  const [form, setForm] = useState({ name: '', unit: 'g', price: 0 });

  useEffect(() => {
    fetchIngredients();
  }, []);

  const fetchIngredients = async () => {
    const res = await api.get('/ingredients');
    setIngredients(res.data);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/ingredients', form);
    setForm({ name: '', unit: 'g', price: 0 });
    fetchIngredients();
  };

  return (
    <div>
      <h2>Składniki</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Nazwa" value={form.name} onChange={handleChange} required />
        <select name="unit" value={form.unit} onChange={handleChange}>
          <option value="g">g</option><option value="kg">kg</option><option value="szt">szt</option>
        </select>
        <input name="price" type="number" step="0.01" placeholder="Cena" value={form.price} onChange={handleChange} required />
        <button type="submit">Dodaj</button>
      </form>
      <ul>
        {ingredients.map((ing) => (
          <li key={ing.id}>{ing.name} - {ing.price} PLN/{ing.unit}</li>
        ))}
      </ul>
    </div>
  );
}