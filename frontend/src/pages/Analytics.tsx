import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '../services';
import { BarChart3, TrendingUp, Users, DollarSign, Calendar, Filter } from 'lucide-react';

export function Analytics() {
  const [dateRange, setDateRange] = useState({ start: '', end: '' });

  const { data: salesData } = useQuery({
    queryKey: ['analytics', 'sales', dateRange],
    queryFn: () => analyticsService.getSalesAnalytics(dateRange),
  });

  const { data: leadData } = useQuery({
    queryKey: ['analytics', 'leads', dateRange],
    queryFn: () => analyticsService.getLeadAnalytics(dateRange),
  });

  const { data: activityData } = useQuery({
    queryKey: ['analytics', 'activities', dateRange],
    queryFn: () => analyticsService.getActivityAnalytics(dateRange),
  });

  const { data: dashboards } = useQuery({
    queryKey: ['analytics', 'dashboards'],
    queryFn: () => analyticsService.getAllDashboards(),
  });

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          <BarChart3 className="w-5 h-5" />
          Create Dashboard
        </button>
      </div>

      <div className="mb-6 flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-gray-500" />
          <input
            type="date"
            value={dateRange.start}
            onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
            className="border rounded-lg px-3 py-2 text-sm"
          />
          <span className="text-gray-500">to</span>
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
            className="border rounded-lg px-3 py-2 text-sm"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="text-sm text-gray-500">Total Revenue</div>
            <DollarSign className="w-5 h-5 text-green-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900">
            ${salesData?.total_revenue?.toLocaleString() || '0'}
          </div>
          <div className="text-sm text-green-600 mt-2">
            +{salesData?.growth_rate || '0'}% from last period
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="text-sm text-gray-500">Total Leads</div>
            <Users className="w-5 h-5 text-blue-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {leadData?.total_leads?.toLocaleString() || '0'}
          </div>
          <div className="text-sm text-blue-600 mt-2">
            {leadData?.conversion_rate || '0'}% conversion rate
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="text-sm text-gray-500">Activities</div>
            <Calendar className="w-5 h-5 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {activityData?.total_activities?.toLocaleString() || '0'}
          </div>
          <div className="text-sm text-purple-600 mt-2">
            {activityData?.completion_rate || '0'}% completed
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="text-sm text-gray-500">Active Deals</div>
            <TrendingUp className="w-5 h-5 text-orange-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900">
            {salesData?.active_deals?.toLocaleString() || '0'}
          </div>
          <div className="text-sm text-orange-600 mt-2">
            ${salesData?.pipeline_value?.toLocaleString() || '0'} pipeline
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Revenue Trend</h2>
          <div className="bg-gray-50 rounded-lg p-8 flex items-center justify-center h-64">
            <div className="text-center text-gray-500">
              <TrendingUp className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p>Revenue chart - Coming soon</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Lead Sources</h2>
          <div className="bg-gray-50 rounded-lg p-8 flex items-center justify-center h-64">
            <div className="text-center text-gray-500">
              <BarChart3 className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p>Lead sources chart - Coming soon</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Your Dashboards</h2>
        {dashboards?.dashboards?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {dashboards.dashboards.map((dashboard: any) => (
              <div key={dashboard.id} className="border rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer">
                <h3 className="font-semibold">{dashboard.name}</h3>
                {dashboard.description && (
                  <p className="text-sm text-gray-500 mt-1">{dashboard.description}</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No dashboards created yet. Create your first dashboard to get started.
          </div>
        )}
      </div>
    </div>
  );
}
