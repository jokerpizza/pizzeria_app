import { useEffect, useState } from 'react'
import api from '../api'

interface Cat{ id:number; name:string }
interface Item{ id?:number; product_id?:number|null; semi_id?:number|null; product_name?:string; semi_name?:string; amount:number; unit:string }
interface Recipe{
  id:number
  name:string
  sale_price:number|null
  is_semi:boolean
  category_id:number|null
  category_name?:string
  items:Item[]
  cost:number
  food_cost_pct:number
  margin:number
  alert:boolean
}
const empty:Recipe={id:0,name:'',sale_price:null,is_semi:false,category_id:null,items:[],cost:0,food_cost_pct:0,margin:0,alert:false}

export default function Recipes(){
  const [recipes,setRecipes]=useState<Recipe[]>([])
  const [products,setProducts]=useState<any[]>([])
  const [cats,setCats]=useState<Cat[]>([])
  const [filter,setFilter]=useState('')
  const [form,setForm]=useState<Recipe>(empty)
  const [editing,setEditing]=useState(false)
  const [sort,setSort]=useState<'name'|'margin'|'fc'|'cost'>('name')
  const [order,setOrder]=useState<'asc'|'desc'>('asc')
  const [fcOnly,setFcOnly]=useState(false)
  const [semiOnly,setSemiOnly]=useState(false)

  const load=()=>{
    api.get('/recipes/', {params:{sort,order,alert_only:fcOnly,only_semi:semiOnly}}).then(r=>setRecipes(r.data))
    api.get('/products/').then(r=>setProducts(r.data))
    api.get('/recipes/', {params:{only_semi:true}}).then(r=>setSemiList(r.data))
    api.get('/categories/recipes').then(r=>setCats(r.data))
  }
  const [semiList,setSemiList]=useState<Recipe[]>([])
  useEffect(()=>{ load() },[sort,order,fcOnly,semiOnly])

  const save=()=>{
    const payload={name:form.name,sale_price:form.sale_price,is_semi:form.is_semi,category_id:form.category_id,
      items:form.items.map(i=>({product_id:i.product_id||null,semi_id:i.semi_id||null,amount:i.amount,unit:i.unit}))}
    if(editing){
      api.put('/recipes/'+form.id,payload).then(()=>{setForm(empty);setEditing(false);load()})
    }else{
      api.post('/recipes/',payload).then(()=>{setForm(empty);load()})
    }
  }

  const del=(id:number)=>{ if(confirm('Usunąć recepturę?')) api.delete('/recipes/'+id).then(load) }

  const addCat=async()=>{
    const name=prompt('Nazwa kat. receptur?')
    if(name){ await api.post('/categories/recipes',{name}); load() }
  }

  const filtered=recipes.filter(r=>r.name.toLowerCase().includes(filter.toLowerCase()))

  const toggleSort=(col:'name'|'margin'|'fc'|'cost')=>{
    if(sort===col) setOrder(order==='asc'?'desc':'asc')
    else{ setSort(col); setOrder('asc') }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Receptury</h1>

      <div className="mb-4 flex flex-wrap gap-2 items-center">
        <input className="border p-2" placeholder="Szukaj..." value={filter} onChange={e=>setFilter(e.target.value)}/>
        <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={fcOnly} onChange={e=>setFcOnly(e.target.checked)}/> FC% &gt; próg</label>
        <label className="flex items-center gap-1 text-sm"><input type="checkbox" checked={semiOnly} onChange={e=>setSemiOnly(e.target.checked)}/> tylko półprodukty</label>
        <button className="bg-brand text-white px-3 py-2 rounded" onClick={addCat}>+ kategoria</button>
      </div>

      <table className="min-w-full bg-white shadow mb-6">
        <thead>
          <tr className="bg-gray-100 text-left">
            <Th onClick={()=>toggleSort('name')}>Nazwa</Th>
            <Th onClick={()=>toggleSort('cost')}>Koszt</Th>
            <Th onClick={()=>toggleSort('fc')}>FC %</Th>
            <Th onClick={()=>toggleSort('margin')}>Marża</Th>
            <th className="p-2">Kat.</th>
            <th className="p-2 w-32"></th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(r=>(
            <tr key={r.id} className={"border-t "+(r.alert?'bg-red-50':'')}>
              <td className="p-2">{r.alert?'⚠️ ':''}{r.name}{r.is_semi?' (półprodukt)':''}</td>
              <td className="p-2">{r.cost.toFixed(2)}</td>
              <td className="p-2">{r.food_cost_pct.toFixed(2)}%</td>
              <td className="p-2">{r.margin.toFixed(2)}</td>
              <td className="p-2">{r.category_name||'-'}</td>
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <input className="border p-2 w-full" placeholder="Nazwa" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>
          <select className="border p-2 w-full" value={form.category_id??''} onChange={e=>setForm({...form,category_id:e.target.value?parseInt(e.target.value):null})}>
            <option value="">(bez kategorii)</option>
            {cats.map(c=><option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={form.is_semi} onChange={e=>setForm({...form,is_semi:e.target.checked})}/>
            Półprodukt
          </label>
          {!form.is_semi && (
            <input className="border p-2 w-full" type="number" step="0.01" placeholder="Cena sprzedaży" value={form.sale_price??''} onChange={e=>setForm({...form,sale_price:e.target.value?parseFloat(e.target.value):null})}/>
          )}
        </div>

        <div>
          <h3 className="font-semibold mb-2">Składniki</h3>
          {form.items.map((it,idx)=>(
            <div key={idx} className="flex flex-wrap gap-2 mb-2">
              <select className="border p-2" value={it.product_id||it.semi_id||''} onChange={e=>{
                const val=e.target.value
                const copy=[...form.items]
                if(val.startsWith('p-')){
                  const id=parseInt(val.slice(2))
                  const name=products.find(p=>p.id===id)?.name
                  copy[idx]={product_id:id,product_name:name,semi_id:null,amount:it.amount,unit:it.unit}
                }else if(val.startsWith('s-')){
                  const id=parseInt(val.slice(2))
                  const name=semiList.find(s=>s.id===id)?.name
                  copy[idx]={semi_id:id,semi_name:name,product_id:null,amount:it.amount,unit:it.unit}
                }else{
                  copy[idx]={product_id:null,semi_id:null,amount:it.amount,unit:it.unit}
                }
                setForm({...form,items:copy})
              }}>
                <option value="">-- wybierz --</option>
                <optgroup label="Produkty">
                  {products.map(p=><option key={'p-'+p.id} value={'p-'+p.id}>{p.name}</option>)}
                </optgroup>
                <optgroup label="Półprodukty">
                  {semiList.map(s=><option key={'s-'+s.id} value={'s-'+s.id}>{s.name}</option>)}
                </optgroup>
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
              <button className="text-red-600" onClick={()=>{ const copy=[...form.items]; copy.splice(idx,1); setForm({...form,items:copy})}}>X</button>
            </div>
          ))}
          <button className="text-green-700" onClick={()=>setForm({...form,items:[...form.items,{product_id:null,semi_id:null,amount:0,unit:'g'}]})}>+ dodaj składnik</button>
        </div>

        <button className="bg-brand text-white px-4 py-2 rounded" onClick={save}>{editing?'Zapisz':'Dodaj'}</button>
        {editing && <button className="ml-2 px-3 py-2" onClick={()=>{setForm(empty);setEditing(false)}}>Anuluj</button>}
      </div>
    </div>
  )
}

function Th({children,onClick}:{children:any,onClick:()=>void}){
  return <th className="p-2 cursor-pointer select-none" onClick={onClick}>{children}</th>
}
