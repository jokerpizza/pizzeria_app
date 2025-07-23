import React, {useEffect, useState} from 'react'
import { api } from '../api/client'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'

type StatPoint={label:string,value:number}
type OrderItem={name:string, quantity:number, price:number}
type Order={id:number, external_id:string, finished_at:string|null, number:string|null, source:string|null, items:OrderItem[]}

export default function Dashboard(){
  const [points,setPoints]=useState<StatPoint[]>([])
  const [orders,setOrders]=useState<Order[]>([])

  const [metrics, setMetrics] = useState<{ date: string; revenue: number; cost: number; profit: number } | null>(null);

  // Fetch today's profit metrics
  useEffect(() => {
    const fetchMetrics = async () => {
      const { data } = await api.get("/api/metrics/today-profit");
      setMetrics(data);
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  // Fetch recent orders
  useEffect(() => {
    const fetchOrders = async () => {
      const { data } = await api.get<Order[]>("/api/orders?limit=20");
      setOrders(data);
    };
    fetchOrders();
  }, []);



  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>Dashboard</h1>
      <div style={{width:'100%',height:300}}>
        <ResponsiveContainer>
          <LineChart data={points}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="label" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <section style={{marginTop:30}}>
        <h2>Ostatnie zamówienia</h2>
        <table style={{width:'100%', borderCollapse:'collapse', fontSize:14}}>
          <thead>
            <tr>
              <th style={{textAlign:'left', borderBottom:'1px solid #ccc'}}>Data</th>
              <th style={{textAlign:'left', borderBottom:'1px solid #ccc'}}>Nr</th>
              <th style={{textAlign:'left', borderBottom:'1px solid #ccc'}}>Źródło</th>
              <th style={{textAlign:'left', borderBottom:'1px solid #ccc'}}>Pozycje</th>
              <th style={{textAlign:'right', borderBottom:'1px solid #ccc'}}>Suma (PLN)</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o=>{
              const sum = o.items.reduce((s,i)=>s + (i.price||0),0)
              return (
                <tr key={o.id}>
                  <td style={{padding:'6px 0'}}>{o.finished_at ? new Date(o.finished_at).toLocaleString() : '-'}</td>
                  <td>{o.number||o.external_id}</td>
                  <td>{o.source||''}</td>
                  <td>{o.items.map((i,idx)=>(<span key={idx}>{i.name} x{i.quantity}{idx<o.items.length-1?', ':''}</span>))}</td>
                  <td style={{textAlign:'right'}}>{sum.toFixed(2)}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </section>
    </div>
  )
}