import { useEffect, useState } from 'react'
import api from '../api'

interface Product{ id:number; name:string; base_unit:string; price_per_kg:number }
interface Item{ id?:number; product_id:number; product_name?:string; amount:number; unit:string }
interface Recipe{
  id:number
  name:string
  sale_price:number
  items:Item[]
  cost:number
  food_cost_pct:number
  margin:number
}

const emptyRecipe:Recipe = {id:0,name:'',sale_price:0,items:[],cost:0,food_cost_pct:0,margin:0}

export default function Recipes(){
  const [recipes,setRecipes]=useState<Recipe[]>([])
  const [products,setProducts]=useState<Product[]>([])
  const [filter,setFilter]=useState('')
  const [form,setForm]=useState<Recipe>(emptyRecipe)
  const [editing,setEditing]=useState(false)

  const load=()=>{
    api.get('/recipes/').then(r=>setRecipes(r.data))
    api.get('/products/').then(r=>setProducts(r.data))
  }
  useEffect(()=>{ load() },[])

  const save=()=>{
    const payload = {name:form.name,sale_price:form.sale_price,items:form.items.map(i=>({product_id:i.product_id,amount:i.amount,unit:i.unit}))}
    if(editing){
      api.put('/recipes/'+form.id, payload).then(()=>{setForm(emptyRecipe);setEditing(false);load()})
    }else{
      api.post('/recipes/', payload).then(()=>{setForm(emptyRecipe);load()})
    }
  }

  const del=(id:number)=>{
    if(confirm('Usunąć recepturę?')) api.delete('/recipes/'+id).then(load)
  }

  const filtered = recipes.filter(r=>r.name.toLowerCase().includes(filter.toLowerCase()))

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Receptury</h1>

      <div className="mb-4 flex gap-2">
        <input className="border p-2 flex-1" placeholder="Szukaj..." value={filter} onChange={e=>setFilter(e.target.value)}/>
      </div>

      <table className="min-w-full bg-white shadow mb-6">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="p-2">Nazwa</th>
            <th className="p-2">Koszt (PLN)</th>
            <th className="p-2">Cena sprz. (PLN)</th>
            <th className="p-2">FC %</th>
            <th className="p-2">Marża (PLN)</th>
            <th className="p-2 w-32"></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(r=>(
            <tr key={r.id} className="border-t">
              <td className="p-2">{r.name}</td>
              <td className="p-2">{r.cost.toFixed(2)}</td>
              <td className="p-2">{r.sale_price.toFixed(2)}</td>
              <td className="p-2">{r.food_cost_pct.toFixed(2)}%</td>
              <td className="p-2">{r.margin.toFixed(2)}</td>
              <td className="p-2 space-x-2">
                <button className="text-blue-600" onClick={()=>{setForm(r);setEditing(true)}}>Edytuj</button>
                <button className="text-red-600" onClick={()=>del(r.id)}>Usuń</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2 className="text-xl font-semibold mb-2">{editing?'Edytuj':'Dodaj'} recepturę</h2>
      <div className="bg-white shadow rounded p-4 space-y-3">
        <input className="border p-2 w-full" placeholder="Nazwa" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>
        <input className="border p-2 w-full" type="number" step="0.01" placeholder="Cena sprzedaży" value={form.sale_price} onChange={e=>setForm({...form,sale_price:parseFloat(e.target.value)})}/>

        <div>
          <h3 className="font-semibold mb-2">Składniki</h3>
          {form.items.map((it,idx)=>(
            <div key={idx} className="flex gap-2 mb-2">
              <select className="border p-2 flex-1" value={it.product_id} onChange={e=>{
                const pid = parseInt(e.target.value)
                const name = products.find(p=>p.id===pid)?.name
                const copy=[...form.items]; copy[idx]={...copy[idx],product_id:pid,product_name:name}
                setForm({...form,items:copy})
              }}>
                <option value="">-- wybierz produkt --</option>
                {products.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}
              </select>
              <input className="border p-2 w-24" type="number" step="0.01" value={it.amount} onChange={e=>{
                const copy=[...form.items]; copy[idx]={...copy[idx],amount:parseFloat(e.target.value)}
                setForm({...form,items:copy})
              }}/>
              <select className="border p-2 w-20" value={it.unit} onChange={e=>{
                const copy=[...form.items]; copy[idx]={...copy[idx],unit:e.target.value}
                setForm({...form,items:copy})
              }}>
                {['kg','g','l','ml','szt'].map(u=><option key={u}>{u}</option>)}
              </select>
              <button className="text-red-600" onClick={()=>{
                const copy=[...form.items]; copy.splice(idx,1); setForm({...form,items:copy})
              }}>X</button>
            </div>
          ))}
          <button className="text-green-700" onClick={()=>setForm({...form,items:[...form.items,{product_id:0,amount:0,unit:'g'}]})}>+ dodaj składnik</button>
        </div>

        <button className="bg-brand text-white px-4 py-2 rounded" onClick={save}>{editing?'Zapisz':'Dodaj'}</button>
        {editing && <button className="ml-2 px-3 py-2" onClick={()=>{setForm(emptyRecipe);setEditing(false)}}>Anuluj</button>}
      </div>
    </div>
  )
}
