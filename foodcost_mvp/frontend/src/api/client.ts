import axios from 'axios';

const baseURL = import.meta.env.VITE_API_URL || 'https://foocostb.onrender.com/api';
export const api = axios.create({ baseURL });
