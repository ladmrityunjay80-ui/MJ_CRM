import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore } from './lib/auth';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Leads from './pages/Leads';
import Contacts from './pages/Contacts';
import Companies from './pages/Companies';
import Deals from './pages/Deals';
import Activities from './pages/Activities';
import Products from './pages/Products';
import DealsKanban from './pages/DealsKanban';
import ActivitiesCalendar from './pages/ActivitiesCalendar';
import Workflows from './pages/Workflows';
import Campaigns from './pages/Campaigns';
import Documents from './pages/Documents';
import Reports from './pages/Reports';
import Integrations from './pages/Integrations';
import Analytics from './pages/Analytics';
import AuditLogs from './pages/AuditLogs';
import Notifications from './pages/Notifications';
import Search from './pages/Search';

const queryClient = new QueryClient();

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((state) => state.token);
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const token = useAuthStore((state) => state.token);
  if (token) {
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            }
          />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="leads" element={<Leads />} />
            <Route path="contacts" element={<Contacts />} />
            <Route path="companies" element={<Companies />} />
            <Route path="deals" element={<Deals />} />
            <Route path="deals-kanban" element={<DealsKanban />} />
            <Route path="activities" element={<Activities />} />
            <Route path="activities-calendar" element={<ActivitiesCalendar />} />
            <Route path="products" element={<Products />} />
            <Route path="workflows" element={<Workflows />} />
            <Route path="campaigns" element={<Campaigns />} />
            <Route path="documents" element={<Documents />} />
            <Route path="reports" element={<Reports />} />
            <Route path="integrations" element={<Integrations />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="audit-logs" element={<AuditLogs />} />
            <Route path="notifications" element={<Notifications />} />
            <Route path="search" element={<Search />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
