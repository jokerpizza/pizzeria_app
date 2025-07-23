
import { useEffect, useState } from 'react'

interface Item {
  id: number
  finished_at: string
  name: string
  qty: number
  turnover: number
  cost: number
  margin: number
  margin_pct: number
}

interface ApiResponse {
  status: string
  count: number
  items: Item[]
  totals: {turnover:number, cost:number, margin:number}
}

export default function Sales(){
  const [data,setData] = useState<ApiResponse|null>(null)
  const [error,setError] = useState<string|null>(null)
  const fetchData = async ()=>{
    try{
      const res = await fetch('/api/sales/live')
      const json = await res.json()
      setData(json)
      setError(null)
    }catch(e){
      setError('Błąd API')
    }
  }
  useEffect(()=>{
    fetchData()
    const id = setInterval(fetchData,15000)
    return ()=>clearInterval(id)
  },[])

  if(error) return <p className="text-red-600">{error}</p>
  if(!data) return <p>Ładowanie…</p>
  if(data.count===0) return <p className="italic text-gray-500">Połączono z Papu — brak sprzedaży w ostatnich 5 minutach.</p>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Sprzedaż LIVE</h1>
      <table className="min-w-full text-sm text-left">
        <thead className="bg-gray-100 text-xs uppercase">
          <tr><th className="px-3 py-2">Czas</th><th className="px-3 py-2">Nazwa</th><th className="px-3 py-2">Qty</th><th className="px-3 py-2">Obrót</th><th className="px-3 py-2">Koszt</th><th className="px-3 py-2">Marża</th><th className="px-3 py-2">% </th></tr>
        </thead>
        <tbody>
          {data.items.map(it=>(
            <tr key={it.id} className="border-b">
              <td className="px-3 py-1 whitespace-nowrap">{new Date(it.finished_at).toLocaleTimeString()}</td>
              <td className="px-3 py-1">{it.name}</td>
              <td className="px-3 py-1 text-right">{it.qty}</td>
              <td className="px-3 py-1 text-right">{it.turnover.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{it.cost.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{it.margin.toFixed(2)}</td>
              <td className="px-3 py-1 text-right">{it.margin_pct.toFixed(1)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
