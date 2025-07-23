import React, { useState } from 'react';
import { Tabs, Tab, Box } from '@mui/material';
import IngredientsPage from './IngredientsPage';
import RecipesPage from './RecipesPage';
import MappingsPage from './MappingsPage';
import OrdersPage from './OrdersPage';

export default function App() {
  const [tab, setTab] = useState(0);
  return (
    <Box sx={{ width: '100%', padding: 2 }}>
      <Tabs value={tab} onChange={(e, v) => setTab(v)}>
        <Tab label="Surowce" />
        <Tab label="Przepisy" />
        <Tab label="Mapowania" />
        <Tab label="Zamówienia" />
      </Tabs>
      {tab === 0 && <IngredientsPage />}
      {tab === 1 && <RecipesPage />}
      {tab === 2 && <MappingsPage />}
      {tab === 3 && <OrdersPage />}
    </Box>
  );
}
