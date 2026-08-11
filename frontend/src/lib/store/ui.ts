import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface UIState {
  sidebarOpen: boolean;
  mobileMenuOpen: boolean;
  modalOpen: boolean;
  activeModal: string | null;
  theme: 'light' | 'dark';
  
  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setMobileMenuOpen: (open: boolean) => void;
  toggleMobileMenu: () => void;
  setModalOpen: (open: boolean, modalId?: string) => void;
  closeModal: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
}

export const useUIStore = create<UIState>()(
  devtools(
    (set) => ({
      sidebarOpen: true,
      mobileMenuOpen: false,
      modalOpen: false,
      activeModal: null,
      theme: 'light',
      
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setMobileMenuOpen: (open) => set({ mobileMenuOpen: open }),
      toggleMobileMenu: () => set((state) => ({ mobileMenuOpen: !state.mobileMenuOpen })),
      setModalOpen: (open, modalId) => set({ modalOpen: open, activeModal: modalId || null }),
      closeModal: () => set({ modalOpen: false, activeModal: null }),
      setTheme: (theme) => set({ theme }),
      toggleTheme: () => set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
    }),
    { name: 'ui-store' }
  )
);
