import { useEffect, useState } from 'react'
import api from '../api'

export default function Settings(){
  const [threshold,setThreshold]=useState<number>(35)

  useEffect(()=>{ api.get('/settings/').then(r=>setThreshold(r.data.fc_threshold)) },[])

  const save=()=>{ api.put('/settings/',{fc_threshold:threshold}).then(()=>alert('Zapisano')) }

  return (
    <div className="max-w-md">
      <h1 className="text-2xl font-semibold mb-4">Ustawienia</h1>
      <label className="block mb-2 text-sm text-gray-600">Próg Food Cost %</label>
      <input className="border p-2 w-full mb-4" type="number" step="0.01" value={threshold} onChange={e=>setThreshold(parseFloat(e.target.value))}/>
      <button className="bg-brand text-white px-4 py-2 rounded" onClick={save}>Zapisz</button>
    </div>
  )
}
