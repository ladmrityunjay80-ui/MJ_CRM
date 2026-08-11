import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ChevronLeft, ChevronRight, Plus, Clock, User, MapPin } from 'lucide-react';
import { format, addMonths, subMonths, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay, isToday } from 'date-fns';
import { activitiesService } from '../services/activities';

interface Activity {
  id: string;
  title: string;
  description: string;
  activity_type: string;
  status: string;
  due_date: string;
  assigned_to_name?: string;
  contact_name?: string;
  deal_name?: string;
}

const ACTIVITY_COLORS = {
  call: 'bg-blue-500',
  meeting: 'bg-purple-500',
  email: 'bg-green-500',
  task: 'bg-yellow-500',
  note: 'bg-gray-500',
};

export default function ActivitiesCalendar() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);

  const { data: activities, isLoading } = useQuery({
    queryKey: ['activities'],
    queryFn: () => activitiesService.getAll(),
  });

  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const calendarDays = eachDayOfInterval({ start: monthStart, end: monthEnd });

  const previousMonth = () => setCurrentDate(subMonths(currentDate, 1));
  const nextMonth = () => setCurrentDate(addMonths(currentDate, 1));

  const getActivitiesForDay = (date: Date) => {
    return activities?.filter((activity: Activity) => 
      isSameDay(new Date(activity.due_date), date)
    ) || [];
  };

  const getActivityColor = (type: string) => {
    return ACTIVITY_COLORS[type as keyof typeof ACTIVITY_COLORS] || 'bg-gray-500';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Activities Calendar</h1>
            <p className="text-gray-600 mt-1">View and manage your scheduled activities</p>
          </div>
          <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            <Plus className="w-5 h-5" />
            New Activity
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="flex items-center justify-between p-4 border-b">
          <button
            onClick={previousMonth}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <h2 className="text-xl font-semibold">
            {format(currentDate, 'MMMM yyyy')}
          </h2>
          <button
            onClick={nextMonth}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>

        <div className="grid grid-cols-7 border-b">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
            <div key={day} className="p-3 text-center font-medium text-gray-600 text-sm">
              {day}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7">
          {calendarDays.map((date) => {
            const dayActivities = getActivitiesForDay(date);
            const isCurrentMonth = isSameMonth(date, currentDate);
            const isDayToday = isToday(date);

            return (
              <div
                key={date.toISOString()}
                className={`min-h-32 p-2 border-r border-b ${
                  !isCurrentMonth ? 'bg-gray-50' : 'bg-white'
                } ${isDayToday ? 'bg-blue-50' : ''}`}
              >
                <div className={`text-sm font-medium mb-2 ${
                  !isCurrentMonth ? 'text-gray-400' : 'text-gray-900'
                } ${isDayToday ? 'text-blue-600' : ''}`}>
                  {format(date, 'd')}
                </div>

                <div className="space-y-1">
                  {dayActivities.slice(0, 3).map((activity: Activity) => (
                    <div
                      key={activity.id}
                      onClick={() => setSelectedActivity(activity)}
                      className={`text-xs p-1 rounded cursor-pointer hover:opacity-80 transition-opacity ${getActivityColor(activity.activity_type)} text-white truncate`}
                    >
                      {activity.title}
                    </div>
                  ))}
                  {dayActivities.length > 3 && (
                    <div className="text-xs text-gray-500">
                      +{dayActivities.length - 3} more
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {selectedActivity && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          onClick={() => setSelectedActivity(null)}
        >
          <div
            className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-semibold">{selectedActivity.title}</h3>
                <button
                  onClick={() => setSelectedActivity(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-2 text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span>{format(new Date(selectedActivity.due_date), 'PPP p')}</span>
                </div>

                {selectedActivity.assigned_to_name && (
                  <div className="flex items-center gap-2 text-gray-600">
                    <User className="w-4 h-4" />
                    <span>{selectedActivity.assigned_to_name}</span>
                  </div>
                )}

                {selectedActivity.contact_name && (
                  <div className="flex items-center gap-2 text-gray-600">
                    <User className="w-4 h-4" />
                    <span>{selectedActivity.contact_name}</span>
                  </div>
                )}

                {selectedActivity.deal_name && (
                  <div className="flex items-center gap-2 text-gray-600">
                    <MapPin className="w-4 h-4" />
                    <span>{selectedActivity.deal_name}</span>
                  </div>
                )}

                {selectedActivity.description && (
                  <div className="text-gray-600 mt-4">
                    {selectedActivity.description}
                  </div>
                )}

                <div className="flex items-center gap-2 mt-4">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getActivityColor(selectedActivity.activity_type)} text-white`}>
                    {selectedActivity.activity_type}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    selectedActivity.status === 'completed' ? 'bg-green-100 text-green-800' :
                    selectedActivity.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {selectedActivity.status}
                  </span>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  Edit
                </button>
                <button className="flex-1 bg-gray-200 text-gray-800 py-2 rounded-lg hover:bg-gray-300 transition-colors">
                  Complete
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
