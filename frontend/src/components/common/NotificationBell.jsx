import { Bell } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function NotificationBell({ count = 0 }) {
  return (
    <Link to="/app/notifications" className="relative p-2 text-gray-500 hover:text-primary-700 transition-colors">
      <Bell className="w-5 h-5" />
      {count > 0 && (
        <span className="absolute -top-0.5 -right-0.5 bg-accent-500 text-white text-[10px] font-bold rounded-full w-4 h-4 flex items-center justify-center">
          {count > 9 ? '9+' : count}
        </span>
      )}
    </Link>
  );
}
