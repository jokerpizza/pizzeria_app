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
      <h1 className="text-2xl font-semibold mb-4">Produkty</h1>
      <form onSubmit={submit} className="flex gap-2 mb-4 flex-wrap">
        <input className="border px-2 py-1" placeholder="nazwa" value={form.name} onChange={e=>setForm({...form, name:e.target.value})}/>
        <input className="border px-2 py-1" placeholder="jednostka" value={form.base_unit} onChange={e=>setForm({...form, base_unit:e.target.value})}/>
        <input className="border px-2 py-1" type="number" step="0.01" placeholder="cena" value={form.price_per_unit}
               onChange={e=>setForm({...form, price_per_unit:parseFloat(e.target.value)})}/>
        <button className="bg-green-600 text-white px-3 py-1 rounded" type="submit">Dodaj</button>
      </form>

      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="border p-2">Nazwa</th>
            <th className="border p-2">Jednostka</th>
            <th className="border p-2">Cena/jedn.</th>
          </tr>
        </thead>
        <tbody>
          {data.map(p => (
            <tr key={p.id}>
              <td className="border p-2">{p.name}</td>
              <td className="border p-2">{p.base_unit}</td>
              <td className="border p-2">{p.price_per_unit.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Products;
