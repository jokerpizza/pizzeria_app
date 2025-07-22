import { useEffect, useState } from 'react'
import api from '../api'
import StatCard from '../components/StatCard'

interface Dash{
  product_count:number
  avg_food_cost_pct:number
  top5_expensive:{name:string,cost:number}[]
  alerts:{name:string,fc:number}[]
}

export default function Dashboard(){
  const [data,setData]=useState<Dash|null>(null)

  useEffect(()=>{ api.get('/dashboard/').then(r=>setData(r.data)) },[])

  if(!data) return <div>Ładowanie...</div>

  return (
    <div className="space-y-6">
      {data.alerts.length>0 && (
        <div className="bg-red-100 border border-red-300 text-red-800 p-3 rounded">
          ⚠️ {data.alerts.length} receptur ma FC% powyżej progu
        </div>
      )}
      <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard title="Liczba produktów" value={data.product_count}/>
        <StatCard title="Średni Food Cost %" value={data.avg_food_cost_pct.toFixed(2)+'%'}/>
        <StatCard title="Top 5 kosztownych" value={data.top5_expensive.length}/>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-2 mt-6">Top 5 najdroższych receptur</h2>
        <table className="min-w-full bg-white shadow">
          <thead><tr className="bg-gray-100 text-left"><th className="p-2">#</th><th className="p-2">Nazwa</th><th className="p-2">Koszt (PLN)</th></tr></thead>
          <tbody>
            {data.top5_expensive.map((r,i)=>(
              <tr key={r.name} className="border-t">
                <td className="p-2">{i+1}</td>
                <td className="p-2">{r.name}</td>
                <td className="p-2">{r.cost.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
