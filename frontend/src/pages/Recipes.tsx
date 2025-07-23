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
    await api.post('/recipes/', { name, portion_size: portion, sale_price: price, items });
    setName(''); setPortion(1); setPrice(0); setItems([]);
    load();
  };

  return (
    <div>
      <h1 style={{fontSize:'1.5rem', fontWeight:600, marginBottom:'1rem'}}>Receptury</h1>

      <form onSubmit={submit} style={{display:'flex', flexDirection:'column', gap:'0.5rem', marginBottom:'1rem'}}>
        <input placeholder="nazwa" value={name} onChange={e=>setName(e.target.value)} />
        <input type="number" step="0.01" placeholder="porcja" value={portion} onChange={e=>setPortion(parseFloat(e.target.value))} />
        <input type="number" step="0.01" placeholder="cena sprzedaży" value={price} onChange={e=>setPrice(parseFloat(e.target.value))} />

        <div style={{border:'1px solid #ccc', padding:'0.5rem'}}>
          <h4 style={{marginBottom:'0.5rem'}}>Składniki</h4>
          {items.map((it, idx)=>(
            <div key={idx} style={{display:'flex', gap:'0.5rem', marginBottom:'0.3rem', flexWrap:'wrap'}}>
              <select value={it.product_id} onChange={e=>updateItem(idx,'product_id',parseInt(e.target.value))}>
                {products.map(p=>(<option key={p.id} value={p.id}>{p.name}</option>))}
              </select>
              <input type="number" step="0.01" placeholder="ilość" value={it.quantity} onChange={e=>updateItem(idx,'quantity',parseFloat(e.target.value))} />
            </div>
          ))}
          <button type="button" onClick={addItem}>+ składnik</button>
        </div>

        <button type="submit">Utwórz recepturę</button>
      </form>

      <table style={{width:'100%', borderCollapse:'collapse'}}>
        <thead>
          <tr style={{background:'#eee', textAlign:'left'}}>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>Nazwa</th>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>Food cost</th>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>%</th>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>Marża</th>
          </tr>
        </thead>
        <tbody>
          {recipes.map(r=>(
            <tr key={r.id}>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{r.name}</td>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{r.food_cost.toFixed(2)}</td>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{r.food_cost_pct.toFixed(2)}%</td>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{r.margin.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Recipes;
