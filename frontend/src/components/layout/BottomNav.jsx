import { NavLink } from 'react-router-dom';
import { Search, Ticket, CalendarRange, Building2, User } from 'lucide-react';
import { t } from '../../i18n';
import { useAuth } from '../../context/AuthContext';

const customerTabs = [
  { to: '/app', icon: Search, label: 'nav.search', end: true },
  { to: '/app/tickets', icon: Ticket, label: 'nav.tickets' },
  { to: '/app/trips', icon: CalendarRange, label: 'nav.planner' },
  { to: '/app/profile', icon: User, label: 'nav.profile' },
];

const agencyTabs = [
  { to: '/app', icon: Search, label: 'nav.search', end: true },
  { to: '/app/agency', icon: Building2, label: 'nav.agency' },
  { to: '/app/tickets', icon: Ticket, label: 'nav.tickets' },
  { to: '/app/profile', icon: User, label: 'nav.profile' },
];

export default function BottomNav() {
  const { user } = useAuth();
  const tabs = user?.role === 'agency_staff' ? agencyTabs : customerTabs;

  return (
    <nav className="bottom-nav">
      <div className="flex items-center justify-around h-14">
        {tabs.map(({ to, icon: Icon, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex flex-col items-center gap-0.5 px-3 py-1.5 rounded-lg transition-colors ${
                isActive
                  ? 'text-primary-700'
                  : 'text-gray-400 hover:text-gray-600'
              }`
            }
          >
            <Icon className="w-5 h-5" />
            <span className="text-[10px] font-medium">{t(label)}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
}
