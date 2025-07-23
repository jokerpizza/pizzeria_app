import React, { useEffect, useState } from 'react';
import api from '../api';

interface Product {
  id: number;
  name: string;
  base_unit: string;
  price_per_unit: number;
}

const Products: React.FC = () => {
  const [data, setData] = useState<Product[]>([]);
  const [form, setForm] = useState({ name:'', base_unit:'kg', price_per_unit:0 });

  const load = async () => {
    const res = await api.get<Product[]>('/products/');
    setData(res.data);
  };
  useEffect(() => { load(); }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post('/products/', form);
    setForm({name:'', base_unit:'kg', price_per_unit:0});
    load();
  };

  return (
    <div>
      <h1 style={{fontSize:'1.5rem', fontWeight:600, marginBottom:'1rem'}}>Produkty</h1>
      <form onSubmit={submit} style={{display:'flex', gap:'0.5rem', marginBottom:'1rem', flexWrap:'wrap'}}>
        <input placeholder="nazwa" value={form.name} onChange={e=>setForm({...form, name:e.target.value})}/>
        <input placeholder="jednostka" value={form.base_unit} onChange={e=>setForm({...form, base_unit:e.target.value})}/>
        <input type="number" step="0.01" placeholder="cena" value={form.price_per_unit}
               onChange={e=>setForm({...form, price_per_unit:parseFloat(e.target.value)})}/>
        <button type="submit">Dodaj</button>
      </form>

      <table style={{width:'100%', borderCollapse:'collapse'}}>
        <thead>
          <tr style={{background:'#eee', textAlign:'left'}}>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>Nazwa</th>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>Jednostka</th>
            <th style={{border:'1px solid #ccc', padding:'4px'}}>Cena/jedn.</th>
          </tr>
        </thead>
        <tbody>
          {data.map(p => (
            <tr key={p.id}>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{p.name}</td>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{p.base_unit}</td>
              <td style={{border:'1px solid #ccc', padding:'4px'}}>{p.price_per_unit.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default Products;
