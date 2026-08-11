import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { notificationsService } from '../services';
import { Bell, Check, CheckCheck, Trash2, Settings, Filter } from 'lucide-react';

export function Notifications() {
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState<'all' | 'unread' | 'read'>('all');
  const queryClient = useQueryClient();

  const { data, isLoading, error } = useQuery({
    queryKey: ['notifications', page, filter],
    queryFn: () => notificationsService.getAll({ 
      page, 
      page_size: 20,
      is_read: filter === 'unread' ? false : filter === 'read' ? true : undefined 
    }),
  });

  const { data: unreadCount } = useQuery({
    queryKey: ['notifications-unread-count'],
    queryFn: notificationsService.getUnreadCount,
  });

  const markAsReadMutation = useMutation({
    mutationFn: notificationsService.markAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notifications-unread-count'] });
    },
  });

  const markAllAsReadMutation = useMutation({
    mutationFn: notificationsService.markAllAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notifications-unread-count'] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: notificationsService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notifications-unread-count'] });
    },
  });

  const handleMarkAsRead = (id: string) => {
    markAsReadMutation.mutate(id);
  };

  const handleMarkAllAsRead = () => {
    markAllAsReadMutation.mutate();
  };

  const handleDelete = (id: string) => {
    deleteMutation.mutate(id);
  };

  const getNotificationIcon = (type: string) => {
    const icons: Record<string, string> = {
      lead: '👤',
      deal: '💰',
      activity: '📅',
      system: '⚙️',
      alert: '🚨',
    };
    return icons[type] || '📬';
  };

  if (isLoading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6">Error loading notifications</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
          {unreadCount?.unread_count > 0 && (
            <span className="bg-red-500 text-white px-3 py-1 rounded-full text-sm">
              {unreadCount.unread_count} unread
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {unreadCount?.unread_count > 0 && (
            <button
              onClick={handleMarkAllAsRead}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              <CheckCheck className="w-5 h-5" />
              Mark All Read
            </button>
          )}
          <button className="flex items-center gap-2 bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300">
            <Settings className="w-5 h-5" />
            Preferences
          </button>
        </div>
      </div>

      <div className="mb-4 flex items-center gap-2">
        <Filter className="w-4 h-4 text-gray-500" />
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg ${filter === 'all' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('unread')}
            className={`px-4 py-2 rounded-lg ${filter === 'unread' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}
          >
            Unread
          </button>
          <button
            onClick={() => setFilter('read')}
            className={`px-4 py-2 rounded-lg ${filter === 'read' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'}`}
          >
            Read
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {data?.notifications?.map((notification: any) => (
          <div
            key={notification.id}
            className={`bg-white rounded-lg shadow p-4 border-l-4 ${
              notification.is_read ? 'border-gray-300' : 'border-blue-500'
            }`}
          >
            <div className="flex items-start gap-4">
              <span className="text-2xl">{getNotificationIcon(notification.notification_type)}</span>
              <div className="flex-1">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className={`font-semibold ${notification.is_read ? 'text-gray-700' : 'text-gray-900'}`}>
                      {notification.title}
                    </h3>
                    <p className="text-gray-600 mt-1">{notification.message}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    {!notification.is_read && (
                      <button
                        onClick={() => handleMarkAsRead(notification.id)}
                        className="text-blue-600 hover:text-blue-900"
                        title="Mark as read"
                      >
                        <Check className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() => handleDelete(notification.id)}
                      className="text-red-600 hover:text-red-900"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div className="text-sm text-gray-500 mt-2">
                  {new Date(notification.created_at).toLocaleString()}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {data?.notifications?.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <Bell className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p>No notifications found</p>
        </div>
      )}
    </div>
  );
}
