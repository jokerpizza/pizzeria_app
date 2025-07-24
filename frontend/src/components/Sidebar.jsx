import { NavLink } from 'react-router-dom'

export default function Sidebar() {
  const links = [
    { to: '/', label: 'Dashboard' },
    { to: '/ingredients', label: 'Składniki' },
    { to: '/recipes', label: 'Receptury' },
  ]
  return (
    <aside className="w-64 bg-white shadow-md flex flex-col">
      <h2 className="text-2xl p-4 font-bold text-green-600">Rentowność</h2>
      <nav className="flex-1">
        {links.map(link => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({isActive})=> 
              'block px-4 py-2 text-lg ' + (isActive?'bg-green-100 text-green-700':'text-gray-700')}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}