import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + '/api',
});

export default api;


// sales
export const fetchSalesLive = async () => {
  const res = await fetch('/api/sales/live')
  return res.json()
}
