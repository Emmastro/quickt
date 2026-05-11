import { t } from '../../i18n';

const STATUS_STYLES = {
  reserved: 'bg-amber-100 text-amber-800',
  confirmed: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
  used: 'bg-gray-100 text-gray-600',
  expired: 'bg-gray-100 text-gray-500',
  pending: 'bg-amber-100 text-amber-800',
  approved: 'bg-green-100 text-green-800',
  suspended: 'bg-red-100 text-red-800',
  scheduled: 'bg-blue-100 text-blue-800',
  boarding: 'bg-indigo-100 text-indigo-800',
  departed: 'bg-purple-100 text-purple-800',
  completed: 'bg-green-100 text-green-700',
};

export default function StatusBadge({ status }) {
  const style = STATUS_STYLES[status] || 'bg-gray-100 text-gray-600';
  return (
    <span className={`status-badge ${style}`}>
      {t(`status.${status}`)}
    </span>
  );
}
