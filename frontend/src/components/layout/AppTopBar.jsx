import { Bus } from 'lucide-react';
import { Link } from 'react-router-dom';
import NotificationBell from '../common/NotificationBell';

export default function AppTopBar() {
  return (
    <header className="app-top-bar">
      <div className="h-full px-4 flex items-center justify-between">
        <Link to="/app" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary-700 rounded-lg flex items-center justify-center">
            <Bus className="w-4 h-4 text-white" />
          </div>
          <span className="text-lg font-bold text-primary-800 tracking-tight">
            Quick<span className="text-accent-500">T</span>
          </span>
        </Link>
        <NotificationBell />
      </div>
    </header>
  );
}
