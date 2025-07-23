import React,{useEffect,useState} from 'react'
import { api } from '../api/client'

type Recipe={id:number,name:string}
type MapRow={id:number,papu_name:string,papu_size?:string,recipe_id:number,recipe_name?:string}

export default function MappingPage(){
  const [unmapped,setUnmapped]=useState<MapRow[]>([])
  const [mapped,setMapped]=useState<MapRow[]>([])
  useEffect(()=>{
    api.get<MapRow[]>('/api/mappings').then(r=>setMapped(r.data))
    api.get<any[]>('/api/orders/?limit=50').then(r=>{
      const names=r.data.flatMap((o:any)=>o.items).map((i:any)=>({papu_name:i.name,papu_size:i.size_name}))
      // filter those not mapped
      setUnmapped(names.filter(n=>!mapped.find(m=>m.papu_name===n.papu_name && m.papu_size===n.papu_size)))
    })
  },[])
  return <div style={{padding:20}}>
    <h2>Mapowanie nazw</h2>
    <div style={{display:'flex',gap:20}}>
      <div style={{flex:1}}>
        <h3>Do zmapowania</h3>
        {unmapped.map((u,i)=><div key={i}>{u.papu_name} {u.papu_size||''}</div>)}
      </div>
      <div style={{flex:1}}>
        <h3>Zmapowane</h3>
        {mapped.map(m=><div key={m.id}>{m.papu_name} → {m.recipe_id}</div>)}
      </div>
    </div>
  </div>
}
