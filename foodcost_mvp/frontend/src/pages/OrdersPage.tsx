import React, { useEffect, useState } from 'react';
import { CRUDTable } from '../components/CRUDTable';
import { api } from '../api/client';
import { TextField } from '@mui/material';

export default function OrdersPage() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/orders?limit=50').then(res => setItems(res.data));
  }, []);
  const columns = [
    { field: 'external_id', headerName: 'Numer' },
    { field: 'vendor', headerName: 'Dostawca' },
    { field: 'created_at', headerName: 'Data' }
  ];
  const renderForm = (item: any, onSubmit: (data:any)=>void) => (
    <>
      <TextField label="Numer" defaultValue={item?.external_id || ''} fullWidth margin="dense" />
      <TextField label="Dostawca" defaultValue={item?.vendor || ''} fullWidth margin="dense" />
      <TextField label="Data" type="datetime-local" defaultValue={item?.created_at || ''} fullWidth margin="dense" />
    </>
  );
  return <CRUDTable resource="Zamówienie" columns={columns} initialData={items} renderForm={renderForm} />;
}
