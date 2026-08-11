import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { integrationsService } from '../services';
import { Plus, Sync, Trash2, Edit, Link, CheckCircle, XCircle, Clock } from 'lucide-react';

export function Integrations() {
  const [page, setPage] = useState(1);
  const [showMarketplace, setShowMarketplace] = useState(false);
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ['integrations', page],
    queryFn: () => integrationsService.getAll({ page, page_size: 10 }),
  });

  const { data: providers } = useQuery({
    queryKey: ['integration-providers'],
    queryFn: integrationsService.getAvailableProviders,
  });

  const deleteMutation = useMutation({
    mutationFn: integrationsService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['integrations'] });
    },
  });

  const syncMutation = useMutation({
    mutationFn: integrationsService.sync,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['integrations'] });
    },
  });

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to remove this integration?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleSync = (id: string) => {
    syncMutation.mutate(id);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      error: 'bg-red-100 text-red-800',
      pending: 'bg-yellow-100 text-yellow-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getProviderIcon = (provider: string) => {
    const icons: Record<string, string> = {
      slack: '💬',
      google: '🔵',
      salesforce: '☁️',
      hubspot: '🟠',
      mailchimp: '🐒',
    };
    return icons[provider] || '🔗';
  };

  if (isLoading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6">Error loading integrations</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Integrations</h1>
        <button
          onClick={() => setShowMarketplace(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5" />
          Browse Marketplace
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Integration
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Provider
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Sync
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data?.integrations?.map((integration: any) => (
              <tr key={integration.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{getProviderIcon(integration.provider)}</span>
                    <div>
                      <div className="text-sm font-medium text-gray-900">{integration.name}</div>
                      {integration.description && (
                        <div className="text-sm text-gray-500">{integration.description}</div>
                      )}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize">
                  {integration.provider}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(integration.status)}`}>
                    {integration.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {integration.last_sync_at ? (
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {new Date(integration.last_sync_at).toLocaleString()}
                    </div>
                  ) : (
                    'Never'
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex items-center justify-end gap-2">
                    <button
                      onClick={() => handleSync(integration.id)}
                      className="text-blue-600 hover:text-blue-900"
                      title="Sync"
                    >
                      <Sync className="w-4 h-4" />
                    </button>
                    <button className="text-gray-600 hover:text-gray-900" title="Edit">
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(integration.id)}
                      className="text-red-600 hover:text-red-900"
                      title="Remove"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showMarketplace && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Integration Marketplace</h2>
              <button
                onClick={() => setShowMarketplace(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {providers?.providers?.map((provider: any) => (
                <div key={provider.id} className="border rounded-lg p-4 hover:shadow-lg transition-shadow">
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-3xl">{getProviderIcon(provider.id)}</span>
                    <div>
                      <h3 className="font-semibold">{provider.name}</h3>
                      <p className="text-sm text-gray-500">{provider.description}</p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1 mb-3">
                    {provider.features?.map((feature: string) => (
                      <span key={feature} className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {feature}
                      </span>
                    ))}
                  </div>
                  <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
                    <Link className="w-4 h-4 inline mr-2" />
                    Connect
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
