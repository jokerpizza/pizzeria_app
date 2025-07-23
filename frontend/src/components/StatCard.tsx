export default function StatCard({title,value}:{title:string,value:any}){
  return <div className="bg-white shadow rounded p-4">
    <div className="text-sm text-gray-500">{title}</div>
    <div className="text-2xl font-bold">{value}</div>
  </div>
}
