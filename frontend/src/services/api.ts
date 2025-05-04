import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Function to get and store token
export const getAndStoreToken = async () => {
  try {
    const response = await api.post('/token/', {
      username: 'admin',
      password: 'admin123'
    });
    const token = response.data.token;
    localStorage.setItem('token', token);
    return token;
  } catch (error) {
    console.error('Error getting token:', error);
    throw error;
  }
};

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const getDevices = async () => {
  const response = await api.get('/devices/devicelist/');
  return response.data;
};

export const getProtocols = async () => {
  const response = await api.get('/devices/protocols/');
  return response.data;
};

export const getResults = async () => {
  const response = await api.get('/devices/results/');
  return response.data;
};

export const getUsers = async () => {
  const response = await api.get('/users/users/');
  return response.data;
};

export default api; 