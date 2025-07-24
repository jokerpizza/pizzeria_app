import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  const linkClass = ({ isActive }) =>
    'block px-4 py-2 rounded ' + (isActive ? 'bg-green-200' : 'hover:bg-green-100');
  return (
    <div className="w-64 bg-white border-r">
      <nav className="p-4 space-y-2">
        <NavLink to="/" className={linkClass}>Dashboard</NavLink>
        <NavLink to="/ingredients" className={linkClass}>Składniki</NavLink>
        <NavLink to="/recipes" className={linkClass}>Receptury</NavLink>
      </nav>
    </div>
  );
}
