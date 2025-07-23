import React, { useState } from 'react';
import IngredientsPage from './IngredientsPage';
import { Tabs, Tab, Box } from '@mui/material';

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
      {/* Next tabs to implement similarly for Recipes, Mappings, Orders */}
    </Box>
  );
}
