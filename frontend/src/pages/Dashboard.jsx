export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-white rounded shadow">Stan magazynów</div>
        <div className="p-4 bg-white rounded shadow">Średni FoodCost</div>
        <div className="p-4 bg-white rounded shadow">Średnia marża</div>
        <div className="p-4 bg-white rounded shadow">Raport sprzedaży</div>
      </div>
    </div>
  )
}