import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { reportsService } from '../services';
import { BarChart3, LineChart, PieChart, Download, Calendar, Filter } from 'lucide-react';

export function Reports() {
  const [selectedReport, setSelectedReport] = useState('sales-performance');
  const [dateRange, setDateRange] = useState({ start: '', end: '' });

  const { data: salesData, isLoading: salesLoading } = useQuery({
    queryKey: ['reports', 'sales-performance', dateRange],
    queryFn: () => reportsService.getSalesPerformance(dateRange),
    enabled: selectedReport === 'sales-performance',
  });

  const { data: leadData, isLoading: leadLoading } = useQuery({
    queryKey: ['reports', 'lead-conversion', dateRange],
    queryFn: () => reportsService.getLeadConversion(dateRange),
    enabled: selectedReport === 'lead-conversion',
  });

  const { data: activityData, isLoading: activityLoading } = useQuery({
    queryKey: ['reports', 'activity-summary', dateRange],
    queryFn: () => reportsService.getActivitySummary(dateRange),
    enabled: selectedReport === 'activity-summary',
  });

  const { data: revenueData, isLoading: revenueLoading } = useQuery({
    queryKey: ['reports', 'revenue-trend', dateRange],
    queryFn: () => reportsService.getRevenueTrend(dateRange),
    enabled: selectedReport === 'revenue-trend',
  });

  const { data: teamData, isLoading: teamLoading } = useQuery({
    queryKey: ['reports', 'team-performance', dateRange],
    queryFn: () => reportsService.getTeamPerformance(dateRange),
    enabled: selectedReport === 'team-performance',
  });

  const isLoading = salesLoading || leadLoading || activityLoading || revenueLoading || teamLoading;

  const reportTypes = [
    { id: 'sales-performance', name: 'Sales Performance', icon: BarChart3 },
    { id: 'lead-conversion', name: 'Lead Conversion', icon: PieChart },
    { id: 'activity-summary', name: 'Activity Summary', icon: LineChart },
    { id: 'revenue-trend', name: 'Revenue Trend', icon: LineChart },
    { id: 'team-performance', name: 'Team Performance', icon: BarChart3 },
  ];

  const currentData = {
    'sales-performance': salesData,
    'lead-conversion': leadData,
    'activity-summary': activityData,
    'revenue-trend': revenueData,
    'team-performance': teamData,
  }[selectedReport];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          <Download className="w-5 h-5" />
          Export
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

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-4">Report Types</h3>
            <div className="space-y-2">
              {reportTypes.map((type) => {
                const Icon = type.icon;
                return (
                  <button
                    key={type.id}
                    onClick={() => setSelectedReport(type.id)}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                      selectedReport === type.id
                        ? 'bg-blue-50 text-blue-600'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {type.name}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow p-6">
            {isLoading ? (
              <div className="text-center py-12">Loading report data...</div>
            ) : (
              <div>
                <h2 className="text-xl font-semibold mb-4">
                  {reportTypes.find((t) => t.id === selectedReport)?.name}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  {currentData && Object.entries(currentData).slice(0, 3).map(([key, value]: [string, any]) => (
                    <div key={key} className="bg-gray-50 rounded-lg p-4">
                      <div className="text-sm text-gray-500 capitalize">{key.replace(/_/g, ' ')}</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {typeof value === 'number' ? value.toLocaleString() : value}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="bg-gray-50 rounded-lg p-8 flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <BarChart3 className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                    <p>Chart visualization - Coming soon</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
