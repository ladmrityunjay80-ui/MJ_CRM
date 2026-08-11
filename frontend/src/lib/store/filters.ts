import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface FiltersState {
  leads: Record<string, any>;
  contacts: Record<string, any>;
  companies: Record<string, any>;
  deals: Record<string, any>;
  activities: Record<string, any>;
  products: Record<string, any>;
  workflows: Record<string, any>;
  campaigns: Record<string, any>;
  documents: Record<string, any>;
  reports: Record<string, any>;
  
  setFilters: (entity: string, filters: Record<string, any>) => void;
  updateFilter: (entity: string, key: string, value: any) => void;
  clearFilters: (entity: string) => void;
  clearAllFilters: () => void;
}

export const useFiltersStore = create<FiltersState>()(
  devtools(
    persist(
      (set) => ({
        leads: {},
        contacts: {},
        companies: {},
        deals: {},
        activities: {},
        products: {},
        workflows: {},
        campaigns: {},
        documents: {},
        reports: {},
        
        setFilters: (entity, filters) => set((state) => ({
          ...state,
          [entity]: filters,
        })),
        
        updateFilter: (entity, key, value) => set((state) => ({
          ...state,
          [entity]: {
            ...state[entity as keyof FiltersState],
            [key]: value,
          },
        })),
        
        clearFilters: (entity) => set((state) => ({
          ...state,
          [entity]: {},
        })),
        
        clearAllFilters: () => set({
          leads: {},
          contacts: {},
          companies: {},
          deals: {},
          activities: {},
          products: {},
          workflows: {},
          campaigns: {},
          documents: {},
          reports: {},
        }),
      }),
      {
        name: 'filters-storage',
      }
    )
  )
);
