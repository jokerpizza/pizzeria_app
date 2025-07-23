
import { useEffect, useState } from 'react';
import api from '../api';

interface SaleItem {
  meal: string;
  qty: number;
  revenue: number;
  cost: number;
  margin: number;
  food_cost_pct: number;
}
interface SalesResp {
  status: string;
  count: number;
  items: SaleItem[];
  totals: {
    qty: number;
    revenue: number;
    cost: number;
    margin: number;
    food_cost_pct: number;
  };
}

export default function Sales(){
  const [data, setData] = useState<SalesResp|null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = () => {
    api.get('/sales/live', { params:{ minutes: 5 }})
      .then(r=>{
        setData(r.data);
        setLoading(false);
      });
  };

  useEffect(()=>{
    fetchData();
    const id = setInterval(fetchData, 15000);
    return () => clearInterval(id);
  },[]);

  if(loading) return <div>Ładowanie...</div>;
  if(!data) return <div>Błąd API</div>;
  if(data.count === 0) return <div className="italic text-gray-500">Połączono z Papu – brak sprzedaży w ostatnich 5 minutach.</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold mb-4">Sprzedaż (ostatnie 5 min)</h1>
      <table className="min-w-full text-sm text-left">
        <thead className="bg-gray-100 text-xs uppercase">
          <tr>
            <th className="px-3 py-2">Danie</th>
            <th className="px-3 py-2 text-right">Qty</th>
            <th className="px-3 py-2 text-right">Obrót PLN</th>
            <th className="px-3 py-2 text-right">Koszt PLN</th>
            <th className="px-3 py-2 text-right">Marża PLN</th>
            <th className="px-3 py-2 text-right">FoodCost %</th>
          </tr>
        </thead>
        <tbody>
          {data.items.map(it=>(
            <tr key={it.meal} className="border-b">
              <td className="px-3 py-1">{it.meal}</td>
              <td className="px-3 py-1 text-right">{it.qty}</td>
              <td className="px-3 py-1 text-right">{it.revenue.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{it.cost.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{it.margin.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{it.food_cost_pct.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
