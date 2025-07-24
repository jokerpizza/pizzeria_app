import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function RecipeModal({ visible, onClose, onSaved }) {
  const [name, setName] = useState('')
  const [category, setCategory] = useState('Pizza')
  const [priceDineIn, setPriceDineIn] = useState('')
  const [priceDelivery, setPriceDelivery] = useState('')
  const [tradeNames, setTradeNames] = useState('')
  const [allIngredients, setAllIngredients] = useState([])
  const [rows, setRows] = useState([{ ingredientId: '', quantity: '' }])

  const api = import.meta.env.VITE_API_URL

  useEffect(() => {
    if (!visible) return
    axios.get(`${api}/ingredients`)
      .then(res => setAllIngredients(res.data))
      .catch(console.error)
  }, [visible])

  const addRow = () =>
    setRows(rs => [...rs, { ingredientId: '', quantity: '' }])

  const removeRow = idx =>
    setRows(rs => rs.filter((_, i) => i !== idx))

  const changeRow = (idx, field, value) =>
    setRows(rs => rs.map((r,i) => i===idx ? { ...r, [field]: value } : r))

  const handleSubmit = async e => {
    e.preventDefault()
    const payload = {
      name,
      category,
      price_dine_in: parseFloat(priceDineIn),
      price_delivery: parseFloat(priceDelivery),
      trade_names: tradeNames.split(',').map(s => s.trim()).filter(Boolean),
      ingredients: rows
        .filter(r => r.ingredientId && r.quantity)
        .map(r => ({
          ingredient_id: parseInt(r.ingredientId),
          quantity: parseFloat(r.quantity)
        }))
    }
    try {
      await axios.post(`${api}/recipes`, payload)
      onSaved()
      onClose()
      setName('')
      setPriceDineIn('')
      setPriceDelivery('')
      setTradeNames('')
      setRows([{ ingredientId:'', quantity:'' }])
    } catch(err) {
      console.error(err)
    }
  }

  if (!visible) return null
  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded shadow-lg w-full max-w-2xl overflow-auto"
      >
        <h2 className="text-xl font-bold mb-4">Dodaj recepturę</h2>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <input
            required
            placeholder="Nazwa"
            className="border p-2"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <select
            className="border p-2"
            value={category}
            onChange={e => setCategory(e.target.value)}
          >
            {['Pizza','Burger','Żeberka','Bar','Inne'].map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <input
            required
            type="number"
            step="0.01"
            placeholder="Cena na miejscu"
            className="border p-2"
            value={priceDineIn}
            onChange={e => setPriceDineIn(e.target.value)}
          />
          <input
            required
            type="number"
            step="0.01"
            placeholder="Cena dowóz"
            className="border p-2"
            value={priceDelivery}
            onChange={e => setPriceDelivery(e.target.value)}
          />
          <input
            placeholder="Nazwy handlowe (oddziel przecinkami)"
            className="border p-2 col-span-2"
            value={tradeNames}
            onChange={e => setTradeNames(e.target.value)}
          />
        </div>

        <h3 className="font-semibold mb-2">Składniki</h3>
        {rows.map((r, idx) => (
          <div key={idx} className="flex space-x-2 mb-2">
            <select
              required
              className="border p-2 flex-1"
              value={r.ingredientId}
              onChange={e => changeRow(idx, 'ingredientId', e.target.value)}
            >
              <option value="">Wybierz składnik</option>
              {allIngredients.map(i => (
                <option key={i.id} value={i.id}>{i.name} ({i.unit})</option>
              ))}
            </select>
            <input
              required
              type="number"
              step="0.01"
              placeholder="Ilość"
              className="border p-2 w-24"
              value={r.quantity}
              onChange={e => changeRow(idx, 'quantity', e.target.value)}
            />
            {idx > 0 && (
              <button
                type="button"
                onClick={() => removeRow(idx)}
                className="text-red-500 px-2"
              >
                ×
              </button>
            )}
          </div>
        ))}
        <button
          type="button"
          onClick={addRow}
          className="text-green-600 mb-4"
        >
          + Dodaj wiersz
        </button>

        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border rounded"
          >
            Anuluj
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-green-500 text-white rounded"
          >
            Zapisz
          </button>
        </div>
      </form>
    </div>
  )
}
