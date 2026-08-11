import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../lib/auth';
import { 
  LayoutDashboard, 
  Users, 
  Building2, 
  DollarSign, 
  Calendar, 
  Package,
  LogOut,
  Menu,
  Workflow,
  Mail,
  FileText,
  BarChart3,
  Link as LinkIcon,
  Bell,
  Search
} from 'lucide-react';
import { useState } from 'react';

const Layout = () => {
  const { user, logout } = useAuthStore();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Leads', href: '/leads', icon: Users },
    { name: 'Contacts', href: '/contacts', icon: Users },
    { name: 'Companies', href: '/companies', icon: Building2 },
    { name: 'Deals', href: '/deals', icon: DollarSign },
    { name: 'Activities', href: '/activities', icon: Calendar },
    { name: 'Products', href: '/products', icon: Package },
    { name: 'Workflows', href: '/workflows', icon: Workflow },
    { name: 'Campaigns', href: '/campaigns', icon: Mail },
    { name: 'Documents', href: '/documents', icon: FileText },
    { name: 'Reports', href: '/reports', icon: BarChart3 },
    { name: 'Integrations', href: '/integrations', icon: LinkIcon },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Audit Logs', href: '/audit-logs', icon: FileText },
    { name: 'Notifications', href: '/notifications', icon: Bell },
    { name: 'Search', href: '/search', icon: Search },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className={`fixed left-0 top-0 z-40 h-screen w-64 bg-white border-r border-gray-200 transition-transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 items-center justify-between border-b border-gray-200 px-6">
            <h1 className="text-xl font-bold text-gray-900">CRM</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-gray-500 hover:text-gray-700"
            >
              <Menu className="h-6 w-6" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 px-3 py-4">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <item.icon className="h-5 w-5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* User info */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-500 text-white font-medium">
                {user?.full_name?.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.full_name}
                </p>
                <p className="text-xs text-gray-500 truncate">{user?.email}</p>
              </div>
              <button
                onClick={logout}
                className="text-gray-400 hover:text-gray-600"
                title="Logout"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className={`transition-all ${sidebarOpen ? 'lg:ml-64' : ''}`}>
        {/* Mobile header */}
        <header className="lg:hidden flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-gray-500 hover:text-gray-700"
          >
            <Menu className="h-6 w-6" />
          </button>
          <h1 className="text-lg font-semibold text-gray-900">CRM</h1>
          <div className="w-6" />
        </header>

        {/* Page content */}
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
