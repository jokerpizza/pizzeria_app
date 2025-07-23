
import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

export default function RecipesPage() {
  const [recipes, setRecipes] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [form, setForm] = useState({
    name: '',
    sale_price: 0,
    category: 'Pizza',
    items: [{ ingredient_id: 0, quantity: 0 }]
  });
  const categories = ['Pizza','Burger','Sałatka','Pancakes','Żeberka i dania','Bar','Pozostałe'];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const [resRec, resIng] = await Promise.all([api.get('/recipes'), api.get('/ingredients')]);
    setRecipes(resRec.data);
    setIngredients(resIng.data);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleItemChange = (index, field, value) => {
    const items = [...form.items];
    items[index][field] = value;
    setForm({ ...form, items });
  };

  const addItem = () => {
    setForm({ ...form, items: [...form.items, { ingredient_id: 0, quantity: 0 }] });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/recipes', form);
    setForm({ name: '', sale_price: 0, category: 'Pizza', items: [{ ingredient_id: 0, quantity: 0 }] });
    fetchData();
  };

  return (
    <div>
      <h2>Receptury</h2>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Nazwa" value={form.name} onChange={handleChange} required />
        <input name="sale_price" type="number" step="0.01" placeholder="Cena sprzedaży" value={form.sale_price} onChange={handleChange} required />
        <select name="category" value={form.category} onChange={handleChange}>
          {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
        </select>
        <h3>Składniki w recepturze</h3>
        {form.items.map((item, idx) => (
          <div key={idx}>
            <select value={item.ingredient_id} onChange={e => handleItemChange(idx, 'ingredient_id', Number(e.target.value))}>
              <option value={0}>Wybierz składnik</option>
              {ingredients.map(ing => <option key={ing.id} value={ing.id}>{ing.name}</option>)}
            </select>
            <input type="number" step="0.01" value={item.quantity} onChange={e => handleItemChange(idx, 'quantity', Number(e.target.value))} placeholder="Ilość" />
          </div>
        ))}
        <button type="button" onClick={addItem}>Dodaj składnik</button>
        <button type="submit">Dodaj recepturę</button>
      </form>
      <ul>
        {recipes.map(rec => (
          <li key={rec.id}>
            {rec.name} - {rec.sale_price} PLN - {rec.category}
            <ul>
              {rec.items.map(it => (
                <li key={it.id}>
                  {ingredients.find(i => i.id === it.ingredient_id)?.name || ''}: {it.quantity}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}
