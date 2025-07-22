import { useEffect, useState } from 'react'
import api from '../api'

interface Cat{ id:number; name:string }
interface Product{
  id:number; name:string; base_unit:string; price_per_kg:number; category_id:number|null; category_name?:string
}
const empty:Product={id:0,name:'',base_unit:'kg',price_per_kg:0,category_id:null}

export default function Products(){
  const [items,setItems]=useState<Product[]>([])
  const [cats,setCats]=useState<Cat[]>([])
  const [filter,setFilter]=useState('')
  const [form,setForm]=useState<Product>(empty)
  const [editing,setEditing]=useState(false)
  const load=()=>{
    api.get('/products/').then(r=>setItems(r.data))
    api.get('/categories/products').then(r=>setCats(r.data))
  }
  useEffect(()=>{load()},[])

  const save=()=>{
    const payload={...form}
    if(editing){
      api.put('/products/'+form.id,payload).then(()=>{setEditing(false);setForm(empty);load()})
    }else{
      api.post('/products/',payload).then(()=>{setForm(empty);load()})
    }
  }
  const del=(id:number)=>{ if(confirm('Usunąć?')) api.delete('/products/'+id).then(load) }

  const addCat=async()=>{
    const name=prompt('Nazwa kategorii?')
    if(name){
      await api.post('/categories/products',{name})
      load()
    }
  }

  const filtered=items.filter(i=>i.name.toLowerCase().includes(filter.toLowerCase()))

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Produkty</h1>

      <div className="mb-4 flex gap-2">
        <input className="border p-2 flex-1" placeholder="Szukaj..." value={filter} onChange={e=>setFilter(e.target.value)}/>
        <button className="bg-brand text-white px-3 py-2 rounded" onClick={addCat}>+ kategoria</button>
      </div>

      <table className="min-w-full bg-white shadow mb-6">
        <thead><tr className="bg-gray-100 text-left">
          <th className="p-2">Nazwa</th><th className="p-2">Kategoria</th><th className="p-2">Jednostka</th><th className="p-2">Cena/kg</th><th className="p-2 w-32"></th>
        </tr></thead>
        <tbody>
          {filtered.map(p=>(
            <tr key={p.id} className="border-t">
              <td className="p-2">{p.name}</td>
              <td className="p-2">{p.category_name||'-'}</td>
              <td className="p-2">{p.base_unit}</td>
              <td className="p-2">{p.price_per_kg.toFixed(2)}</td>
              <td className="p-2 space-x-2">
                <button className="text-blue-600" onClick={()=>{setForm(p);setEditing(true)}}>Edytuj</button>
                <button className="text-red-600" onClick={()=>del(p.id)}>Usuń</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 className="text-xl font-semibold mb-2">{editing?'Edytuj':'Dodaj'} produkt</h2>
      <div className="bg-white shadow rounded p-4 max-w-md space-y-3">
        <input className="border p-2 w-full" placeholder="Nazwa" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>
        <select className="border p-2 w-full" value={form.category_id??''} onChange={e=>setForm({...form,category_id:e.target.value?parseInt(e.target.value):null})}>
          <option value="">(bez kategorii)</option>
          {cats.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <select className="border p-2 w-full" value={form.base_unit} onChange={e=>setForm({...form,base_unit:e.target.value})}>
          {['kg','g','l','ml','szt'].map(u=><option key={u}>{u}</option>)}
        </select>
        <input className="border p-2 w-full" type="number" step="0.01" placeholder="Cena za kg" value={form.price_per_kg} onChange={e=>setForm({...form,price_per_kg:parseFloat(e.target.value)})}/>
        <button className="bg-brand text-white px-4 py-2 rounded" onClick={save}>{editing?'Zapisz':'Dodaj'}</button>
        {editing && <button className="ml-2 px-3 py-2" onClick={()=>{setForm(empty);setEditing(false)}}>Anuluj</button>}
      </div>
    </div>
  )
}
