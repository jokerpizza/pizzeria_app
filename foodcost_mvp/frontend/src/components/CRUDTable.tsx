import React, { useState } from 'react';
import { Box, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Table, TableHead, TableRow, TableCell, TableBody, TablePagination } from '@mui/material';

interface CRUDTableProps<T> {
  resource: string;
  columns: { field: string; headerName: string; }[];
  initialData: T[];
  renderForm: (item: T | null, onSubmit: (data: any) => void) => React.ReactNode;
}

export function CRUDTable<T extends { id: number }>({ resource, columns, initialData, renderForm }: CRUDTableProps<T>) {
  const [data, setData] = useState<T[]>(initialData);
  const [filterName, setFilterName] = useState('');
  const [filterDate, setFilterDate] = useState('');
  const [filterPrice, setFilterPrice] = useState('');
  const [page, setPage] = useState(0);
  const [openForm, setOpenForm] = useState(false);
  const [editItem, setEditItem] = useState<T | null>(null);

  const handleFilter = () => {
    return data.filter(item => {
      const byName = filterName ? (item as any).name.toLowerCase().includes(filterName.toLowerCase()) : true;
      const byDate = filterDate ? (item as any).created_at.startsWith(filterDate) : true;
      const byPrice = filterPrice ? ((item as any).price || 0) <= parseFloat(filterPrice) : true;
      return byName && byDate && filterPrice && byPrice || (byName && byDate && !filterPrice);
    });
  };

  const filtered = handleFilter();
  const rowsPerPage = 50;
  const paginated = filtered.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  return (
    <Box>
      <Box mb={2} display="flex" gap={2}>
        <TextField label="Nazwa" value={filterName} onChange={e => setFilterName(e.target.value)} />
        <TextField label="Data utworzenia" type="date" value={filterDate} onChange={e => setFilterDate(e.target.value)} />
        <TextField label="Max cena" type="number" value={filterPrice} onChange={e => setFilterPrice(e.target.value)} />
        <Button variant="contained" onClick={() => { setEditItem(null); setOpenForm(true); }}>+ Dodaj</Button>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            {columns.map(col => <TableCell key={col.field}>{col.headerName}</TableCell>)}
            <TableCell>Akcje</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {paginated.map(row => (
            <TableRow key={row.id}>
              {columns.map(col => <TableCell key={col.field}>{(row as any)[col.field]}</TableCell>)}
              <TableCell>
                <Button size="small" onClick={() => { setEditItem(row); setOpenForm(true); }}>Edytuj</Button>
                <Button size="small" color="error">Usuń</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <TablePagination
        component="div"
        count={filtered.length}
        page={page}
        onPageChange={(e, newPage) => setPage(newPage)}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[rowsPerPage]}
      />
      <Dialog open={openForm} onClose={() => setOpenForm(false)} maxWidth="sm" fullWidth>
        <DialogTitle>{editItem ? 'Edytuj' : 'Dodaj'} {resource}</DialogTitle>
        <DialogContent>
          {renderForm(editItem, (data) => {
            // TODO: implement submit logic with api.post, api.put, api.delete
            setOpenForm(false);
          })}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenForm(false)}>Anuluj</Button>
          <Button onClick={() => { /* call submit */ }}>Zapisz</Button>
        </DialogActions>
      </Dialog>
    </Box>
); }
