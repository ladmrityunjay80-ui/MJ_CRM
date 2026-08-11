import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import api from './api';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  organization_id?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

interface RegisterData {
  email: string;
  password: string;
  full_name: string;
  phone?: string;
  role?: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isLoading: false,

      login: async (email: string, password: string) => {
        console.log('Login attempt started for:', email);
        set({ isLoading: true });
        try {
          const formData = new FormData();
          formData.append('username', email);
          formData.append('password', password);

          console.log('Sending login request to:', '/auth/login');
          console.log('API base URL:', import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1');
          
          const response = await api.post('/auth/login', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });

          console.log('Login response:', response.data);
          const { access_token, user } = response.data;
          localStorage.setItem('access_token', access_token);
          set({ user, token: access_token, isLoading: false });
          console.log('Login successful');
        } catch (error: any) {
          console.error('Login error:', error);
          console.error('Error response:', error.response);
          console.error('Error message:', error.message);
          console.error('Error code:', error.code);
          set({ isLoading: false });
          throw error;
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true });
        try {
          const response = await api.post('/auth/register', data);
          set({ isLoading: false });
          return response.data;
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: () => {
        localStorage.removeItem('access_token');
        set({ user: null, token: null });
      },

      fetchUser: async () => {
        try {
          const response = await api.get('/auth/me');
          set({ user: response.data });
        } catch (error) {
          set({ user: null, token: null });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, token: state.token }),
    }
  )
);
