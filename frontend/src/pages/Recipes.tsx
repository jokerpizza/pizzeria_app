import React, { useEffect, useState } from 'react';
import api from '../api';

interface Product {
  id: number;
  name: string;
  price_per_unit: number;
  base_unit: string;
}

interface RecipeItemCreate {
  product_id: number;
  quantity: number;
}

interface RecipeOut {
  id: number;
  name: string;
  portion_size: number;
  sale_price: number;
  food_cost: number;
  food_cost_pct: number;
  margin: number;
  items: {
    id: number;
    product_id: number;
    quantity: number;
    product: Product;
  }[];
}

const Recipes: React.FC = () => {
  const [recipes, setRecipes] = useState<RecipeOut[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [name, setName] = useState('');
  const [portion, setPortion] = useState(1);
  const [price, setPrice] = useState(0);
  const [items, setItems] = useState<RecipeItemCreate[]>([]);

  const load = async () => {
    const r = await api.get<RecipeOut[]>('/recipes/');
    const p = await api.get<Product[]>('/products/');
    setRecipes(r.data);
    setProducts(p.data);
  };

  useEffect(() => { load(); }, []);

  const addItem = () => setItems([...items, {product_id: products[0]?.id || 0, quantity: 0}]);

  const updateItem = (i:number, field:'product_id'|'quantity', value:any) => {
    const copy = [...items];
    copy[i] = {...copy[i], [field]: value};
    setItems(copy);
  };

  const submit = async (e:React.FormEvent) => {
    e.preventDefault();
    await api.post('/recipes/', {
      name, portion_size: portion, sale_price: price, items
    });
    setName(''); setPortion(1); setPrice(0); setItems([]);
    load();
  };

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Receptury</h1>

      <form onSubmit={submit} className="flex flex-col gap-2 mb-4">
        <input className="border px-2 py-1" placeholder="nazwa" value={name} onChange={e=>setName(e.target.value)} />
        <input className="border px-2 py-1" type="number" step="0.01" placeholder="porcja" value={portion} onChange={e=>setPortion(parseFloat(e.target.value))} />
        <input className="border px-2 py-1" type="number" step="0.01" placeholder="cena sprzedaży" value={price} onChange={e=>setPrice(parseFloat(e.target.value))} />

        <div className="border p-2 rounded">
          <h4 className="font-semibold mb-2">Składniki</h4>
          {items.map((it, idx)=>(
            <div key={idx} className="flex gap-2 mb-2 flex-wrap">
              <select className="border px-2 py-1" value={it.product_id} onChange={e=>updateItem(idx,'product_id',parseInt(e.target.value))}>
                {products.map(p=>(<option key={p.id} value={p.id}>{p.name}</option>))}
              </select>
              <input className="border px-2 py-1" type="number" step="0.01" placeholder="ilość" value={it.quantity} onChange={e=>updateItem(idx,'quantity',parseFloat(e.target.value))} />
            </div>
          ))}
          <button type="button" className="bg-gray-200 px-2 py-1 rounded" onClick={addItem}>+ składnik</button>
        </div>

        <button className="bg-green-600 text-white px-3 py-1 rounded" type="submit">Utwórz recepturę</button>
      </form>

      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="border p-2">Nazwa</th>
            <th className="border p-2">Food cost</th>
            <th className="border p-2">%</th>
            <th className="border p-2">Marża</th>
          </tr>
        </thead>
        <tbody>
          {recipes.map(r=>(
            <tr key={r.id}>
              <td className="border p-2">{r.name}</td>
              <td className="border p-2">{r.food_cost.toFixed(2)}</td>
              <td className="border p-2">{r.food_cost_pct.toFixed(2)}%</td>
              <td className="border p-2">{r.margin.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Recipes;
