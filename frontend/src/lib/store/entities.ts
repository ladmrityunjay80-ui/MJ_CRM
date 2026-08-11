import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface EntitiesState {
  leads: any[];
  contacts: any[];
  companies: any[];
  deals: any[];
  activities: any[];
  products: any[];
  workflows: any[];
  campaigns: any[];
  documents: any[];
  notifications: any[];
  
  setLeads: (leads: any[]) => void;
  addLead: (lead: any) => void;
  updateLead: (id: string, lead: any) => void;
  removeLead: (id: string) => void;
  
  setContacts: (contacts: any[]) => void;
  addContact: (contact: any) => void;
  updateContact: (id: string, contact: any) => void;
  removeContact: (id: string) => void;
  
  setCompanies: (companies: any[]) => void;
  addCompany: (company: any) => void;
  updateCompany: (id: string, company: any) => void;
  removeCompany: (id: string) => void;
  
  setDeals: (deals: any[]) => void;
  addDeal: (deal: any) => void;
  updateDeal: (id: string, deal: any) => void;
  removeDeal: (id: string) => void;
  
  setActivities: (activities: any[]) => void;
  addActivity: (activity: any) => void;
  updateActivity: (id: string, activity: any) => void;
  removeActivity: (id: string) => void;
  
  setProducts: (products: any[]) => void;
  addProduct: (product: any) => void;
  updateProduct: (id: string, product: any) => void;
  removeProduct: (id: string) => void;
  
  setWorkflows: (workflows: any[]) => void;
  addWorkflow: (workflow: any) => void;
  updateWorkflow: (id: string, workflow: any) => void;
  removeWorkflow: (id: string) => void;
  
  setCampaigns: (campaigns: any[]) => void;
  addCampaign: (campaign: any) => void;
  updateCampaign: (id: string, campaign: any) => void;
  removeCampaign: (id: string) => void;
  
  setDocuments: (documents: any[]) => void;
  addDocument: (document: any) => void;
  updateDocument: (id: string, document: any) => void;
  removeDocument: (id: string) => void;
  
  setNotifications: (notifications: any[]) => void;
  addNotification: (notification: any) => void;
  markNotificationAsRead: (id: string) => void;
  removeNotification: (id: string) => void;
  
  clearAll: () => void;
}

export const useEntitiesStore = create<EntitiesState>()(
  devtools(
    persist(
      (set) => ({
        leads: [],
        contacts: [],
        companies: [],
        deals: [],
        activities: [],
        products: [],
        workflows: [],
        campaigns: [],
        documents: [],
        notifications: [],
        
        setLeads: (leads) => set({ leads }),
        addLead: (lead) => set((state) => ({ leads: [...state.leads, lead] })),
        updateLead: (id, lead) => set((state) => ({
          leads: state.leads.map((l) => l.id === id ? { ...l, ...lead } : l)
        })),
        removeLead: (id) => set((state) => ({
          leads: state.leads.filter((l) => l.id !== id)
        })),
        
        setContacts: (contacts) => set({ contacts }),
        addContact: (contact) => set((state) => ({ contacts: [...state.contacts, contact] })),
        updateContact: (id, contact) => set((state) => ({
          contacts: state.contacts.map((c) => c.id === id ? { ...c, ...contact } : c)
        })),
        removeContact: (id) => set((state) => ({
          contacts: state.contacts.filter((c) => c.id !== id)
        })),
        
        setCompanies: (companies) => set({ companies }),
        addCompany: (company) => set((state) => ({ companies: [...state.companies, company] })),
        updateCompany: (id, company) => set((state) => ({
          companies: state.companies.map((c) => c.id === id ? { ...c, ...company } : c)
        })),
        removeCompany: (id) => set((state) => ({
          companies: state.companies.filter((c) => c.id !== id)
        })),
        
        setDeals: (deals) => set({ deals }),
        addDeal: (deal) => set((state) => ({ deals: [...state.deals, deal] })),
        updateDeal: (id, deal) => set((state) => ({
          deals: state.deals.map((d) => d.id === id ? { ...d, ...deal } : d)
        })),
        removeDeal: (id) => set((state) => ({
          deals: state.deals.filter((d) => d.id !== id)
        })),
        
        setActivities: (activities) => set({ activities }),
        addActivity: (activity) => set((state) => ({ activities: [...state.activities, activity] })),
        updateActivity: (id, activity) => set((state) => ({
          activities: state.activities.map((a) => a.id === id ? { ...a, ...activity } : a)
        })),
        removeActivity: (id) => set((state) => ({
          activities: state.activities.filter((a) => a.id !== id)
        })),
        
        setProducts: (products) => set({ products }),
        addProduct: (product) => set((state) => ({ products: [...state.products, product] })),
        updateProduct: (id, product) => set((state) => ({
          products: state.products.map((p) => p.id === id ? { ...p, ...product } : p)
        })),
        removeProduct: (id) => set((state) => ({
          products: state.products.filter((p) => p.id !== id)
        })),
        
        setWorkflows: (workflows) => set({ workflows }),
        addWorkflow: (workflow) => set((state) => ({ workflows: [...state.workflows, workflow] })),
        updateWorkflow: (id, workflow) => set((state) => ({
          workflows: state.workflows.map((w) => w.id === id ? { ...w, ...workflow } : w)
        })),
        removeWorkflow: (id) => set((state) => ({
          workflows: state.workflows.filter((w) => w.id !== id)
        })),
        
        setCampaigns: (campaigns) => set({ campaigns }),
        addCampaign: (campaign) => set((state) => ({ campaigns: [...state.campaigns, campaign] })),
        updateCampaign: (id, campaign) => set((state) => ({
          campaigns: state.campaigns.map((c) => c.id === id ? { ...c, ...campaign } : c)
        })),
        removeCampaign: (id) => set((state) => ({
          campaigns: state.campaigns.filter((c) => c.id !== id)
        })),
        
        setDocuments: (documents) => set({ documents }),
        addDocument: (document) => set((state) => ({ documents: [...state.documents, document] })),
        updateDocument: (id, document) => set((state) => ({
          documents: state.documents.map((d) => d.id === id ? { ...d, ...document } : d)
        })),
        removeDocument: (id) => set((state) => ({
          documents: state.documents.filter((d) => d.id !== id)
        })),
        
        setNotifications: (notifications) => set({ notifications }),
        addNotification: (notification) => set((state) => ({ notifications: [...state.notifications, notification] })),
        markNotificationAsRead: (id) => set((state) => ({
          notifications: state.notifications.map((n) => n.id === id ? { ...n, is_read: true } : n)
        })),
        removeNotification: (id) => set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== id)
        })),
        
        clearAll: () => set({
          leads: [],
          contacts: [],
          companies: [],
          deals: [],
          activities: [],
          products: [],
          workflows: [],
          campaigns: [],
          documents: [],
          notifications: [],
        }),
      }),
      {
        name: 'entities-storage',
        partialize: (state) => ({
          leads: state.leads,
          contacts: state.contacts,
          companies: state.companies,
          deals: state.deals,
        }),
      }
    )
  )
);
