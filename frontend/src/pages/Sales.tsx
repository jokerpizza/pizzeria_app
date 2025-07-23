
import { useEffect, useState } from 'react'
import { fetchSalesLive } from '../api'

interface SaleItem {
  id: number
  finished_at: string
  name: string
  qty: number
  turnover: number
  cost: number
  margin: number
  margin_pct: number
}

const Sales = () => {
  const [items, setItems] = useState<SaleItem[]>([])
  const [count, setCount] = useState(0)

  const load = async () => {
    const res = await fetchSalesLive()
    if(res.status==='ok'){
      setCount(res.count)
      setItems(res.items)
    }
  }

  useEffect(() => {
    load()
    const iv = setInterval(load,15000)
    return ()=>clearInterval(iv)
  },[])

  if(count===0){
    return <p className="p-4 italic text-gray-500">Połączono z Papu – brak sprzedaży w ostatnich 5 minutach.</p>
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Sprzedaż</h1>
      <table className="min-w-full text-sm text-left text-gray-700">
        <thead className="text-xs uppercase bg-gray-100">
          <tr>
            <th className="px-3 py-2">Czas</th><th className="px-3 py-2">Nazwa</th>
            <th className="px-3 py-2">Qty</th><th className="px-3 py-2">Obrót</th>
            <th className="px-3 py-2">Koszt</th><th className="px-3 py-2">Marża</th>
            <th className="px-3 py-2">% </th>
          </tr>
        </thead>
        <tbody>
          {items.map(r=>(
            <tr key={r.id} className="border-b">
              <td className="px-3 py-1">{new Date(r.finished_at).toLocaleTimeString()}</td>
              <td className="px-3 py-1">{r.name}</td>
              <td className="px-3 py-1 text-right">{r.qty}</td>
              <td className="px-3 py-1 text-right">{r.turnover.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{r.cost.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{r.margin.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{r.margin_pct.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Sales
