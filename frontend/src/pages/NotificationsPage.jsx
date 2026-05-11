import { Bell, CheckCheck } from 'lucide-react';
import { t } from '../i18n';
import { useNotifications, useMarkAllRead } from '../hooks/useNotifications';
import { formatDate } from '../utils/format';

export default function NotificationsPage() {
  const { data, isLoading } = useNotifications();
  const markAllRead = useMarkAllRead();

  const notifications = data?.items || [];
  const unreadCount = data?.unread_count || 0;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-bold text-gray-900">Notifications</h1>
        {unreadCount > 0 && (
          <button
            onClick={() => markAllRead.mutate()}
            className="flex items-center gap-1.5 text-sm text-primary-600 font-medium hover:text-primary-800"
          >
            <CheckCheck className="w-4 h-4" />
            Tout lire
          </button>
        )}
      </div>

      {notifications.length === 0 ? (
        <div className="card p-8 text-center">
          <Bell className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">Aucune notification</p>
        </div>
      ) : (
        <div className="space-y-2">
          {notifications.map((notif) => (
            <div
              key={notif.id}
              className={`card p-4 ${!notif.is_read ? 'border-l-4 border-l-primary-500 bg-primary-50/50' : ''}`}
            >
              <div className="flex items-start justify-between mb-1">
                <h3 className={`text-sm font-medium ${notif.is_read ? 'text-gray-700' : 'text-gray-900'}`}>
                  {notif.title}
                </h3>
                {!notif.is_read && (
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-1.5 flex-shrink-0" />
                )}
              </div>
              <p className="text-sm text-gray-500 mb-1">{notif.body}</p>
              <span className="text-xs text-gray-400">{formatDate(notif.created_at)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
