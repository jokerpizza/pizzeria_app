import { useEffect, useState, useMemo } from 'react'
import client from '../api/client'

interface OrderItem {
  ingredient_id: number
  quantity: number
}

interface Order {
  id: number
  date: string
  total_cost: number
  items?: OrderItem[]
}

export default function Dashboard() {
  const [orders, setOrders] = useState<Order[]>([])

  useEffect(() => {
    client.get<Order[]>('/orders/')
      .then(res => {
        // Sort by date descending and take the latest 10 orders
        const latest = res.data
          .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
          .slice(0, 10)
        setOrders(latest)
      })
      .catch(err => console.error('Error fetching orders:', err))
  }, [])

  // Compute today's revenue and profit (70% of revenue)
  const todayRevenue = useMemo(() => {
    const todayString = new Date().toISOString().split('T')[0]
    return orders
      .filter(o => o.date.startsWith(todayString))
      .reduce((sum, o) => sum + o.total_cost, 0)
  }, [orders])

  const todayProfit = useMemo(() => {
    return todayRevenue * 0.7
  }, [todayRevenue])

  return (
    <div className="p-4 space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-white border rounded-lg shadow">
          <div className="text-sm text-gray-500">Dzisiejszy utarg</div>
          <div className="text-2xl font-bold">{todayRevenue.toFixed(2)} PLN</div>
        </div>
        <div className="p-4 bg-white border rounded-lg shadow">
          <div className="text-sm text-gray-500">Dzisiejszy zarobek (70%)</div>
          <div className="text-2xl font-bold">{todayProfit.toFixed(2)} PLN</div>
        </div>
      </div>

      <h1 className="text-xl font-semibold">Ostatnie 10 zamówień</h1>
      {orders.length === 0 ? (
        <p>Brak zamówień do wyświetlenia.</p>
      ) : (
        <ul className="space-y-3">
          {orders.map(o => (
            <li key={o.id} className="p-3 border rounded-lg shadow">
              <div className="font-medium">
                Zamówienie #{o.id} - {new Date(o.date).toLocaleDateString('pl-PL')}
              </div>
              <div>Koszt: {o.total_cost.toFixed(2)} PLN</div>
              {o.items && o.items.length > 0 && (
                <ul className="mt-2 list-disc list-inside">
                  {o.items.map(item => (
                    <li key={item.ingredient_id}>
                      Surowiec ID {item.ingredient_id}: {item.quantity}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
