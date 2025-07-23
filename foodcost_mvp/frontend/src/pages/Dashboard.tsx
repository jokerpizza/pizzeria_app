import React from 'react';
import FilterBar from '../components/FilterBar';
import SalesChart from '../components/SalesChart';
import SalesSummary from '../components/SalesSummary';
import OpenAccounts from '../components/OpenAccounts';
import CashBalance from '../components/CashBalance';
import RecentDocuments from '../components/RecentDocuments';

export default function Dashboard() {
  return (
    <div style={{ padding: 16, maxWidth: 1200, margin: '0 auto' }}>
      <FilterBar />
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
        <SalesChart />
        <SalesSummary />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginTop: 16 }}>
        <OpenAccounts />
        <CashBalance />
        <RecentDocuments />
      </div>
    </div>
  );
}