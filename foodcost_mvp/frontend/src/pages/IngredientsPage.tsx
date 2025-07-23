import React, { useEffect, useState } from 'react';
import { CRUDTable } from '../components/CRUDTable';
import { api } from '../api/client';
import { TextField } from '@mui/material';

export default function IngredientsPage() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/ingredients').then(res => setItems(res.data));
  }, []);
  const columns = [
    { field: 'name', headerName: 'Nazwa' },
    { field: 'unit', headerName: 'Jednostka' },
    { field: 'price', headerName: 'Cena' },
    { field: 'created_at', headerName: 'Data' }
  ];
  const renderForm = (item: any, onSubmit: (data: any) => void) => (
    <>
      <TextField label="Nazwa" defaultValue={item?.name || ''} fullWidth margin="dense" />
      <TextField label="Jednostka" defaultValue={item?.unit || ''} fullWidth margin="dense" />
      <TextField label="Cena" type="number" defaultValue={item?.price || ''} fullWidth margin="dense" />
    </>
  );
  return <CRUDTable resource="Surowiec" columns={columns} initialData={items} renderForm={renderForm} />;
}
