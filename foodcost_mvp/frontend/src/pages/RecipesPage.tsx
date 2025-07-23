import React, { useEffect, useState } from 'react';
import { CRUDTable } from '../components/CRUDTable';
import { api } from '../api/client';
import { TextField } from '@mui/material';

export default function RecipesPage() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/recipes').then(res => setItems(res.data));
  }, []);
  const columns = [
    { field: 'id', headerName: 'ID' },
    { field: 'name', headerName: 'Nazwa' },
    { field: 'created_at', headerName: 'Data' }
  ];
  const renderForm = (item: any, onSubmit: (data:any)=>void) => (
    <>
      <TextField label="Nazwa" defaultValue={item?.name || ''} fullWidth margin="dense" />
    </>
  );
  return <CRUDTable resource="Przepis" columns={columns} initialData={items} renderForm={renderForm} />;
}
