import { useQuery } from '@tanstack/react-query';
import { leadsService, dealsService, activitiesService } from '../services';
import { Users, DollarSign, Calendar, TrendingUp } from 'lucide-react';

const Dashboard = () => {
  const { data: leadsData } = useQuery({
    queryKey: ['leads'],
    queryFn: () => leadsService.getAll({ page_size: 1 }),
  });

  const { data: dealsData } = useQuery({
    queryKey: ['deals'],
    queryFn: () => dealsService.getAll({ page_size: 1 }),
  });

  const { data: activitiesData } = useQuery({
    queryKey: ['activities'],
    queryFn: () => activitiesService.getAll({ page_size: 1 }),
  });

  const stats = [
    {
      name: 'Total Leads',
      value: leadsData?.total || 0,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      name: 'Active Deals',
      value: dealsData?.total || 0,
      icon: DollarSign,
      color: 'bg-green-500',
    },
    {
      name: 'Activities',
      value: activitiesData?.total || 0,
      icon: Calendar,
      color: 'bg-purple-500',
    },
    {
      name: 'Win Rate',
      value: '75%',
      icon: TrendingUp,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
              </div>
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <p className="text-gray-600">No recent activity to display.</p>
      </div>
    </div>
  );
};

export default Dashboard;
