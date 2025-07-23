import React, { useEffect, useState } from 'react';
import { CRUDTable } from '../components/CRUDTable';
import { api } from '../api/client';
import { TextField } from '@mui/material';

export default function MappingsPage() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => {
    api.get('/api/mappings').then(res => setItems(res.data));
  }, []);
  const columns = [
    { field: 'external_name', headerName: 'Nazwa zewnętrzna' },
    { field: 'recipe_id', headerName: 'ID przepisu' }
  ];
  const renderForm = (item: any, onSubmit: (data:any)=>void) => (
    <>
      <TextField label="Nazwa zewnętrzna" defaultValue={item?.external_name || ''} fullWidth margin="dense" />
      <TextField label="ID przepisu" type="number" defaultValue={item?.recipe_id || ''} fullWidth margin="dense" />
    </>
  );
  return <CRUDTable resource="Mapowanie" columns={columns} initialData={items} renderForm={renderForm} />;
}
