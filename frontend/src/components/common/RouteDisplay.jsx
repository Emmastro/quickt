import { MapPin, ArrowRight, Clock } from 'lucide-react';
import { formatDuration } from '../../utils/format';

export default function RouteDisplay({
  origin,
  destination,
  distanceKm,
  durationMinutes,
  compact = false,
}) {
  if (compact) {
    return (
      <div className="flex items-center gap-2 text-sm">
        <span className="font-medium text-gray-900">{origin}</span>
        <ArrowRight className="w-4 h-4 text-primary-400" />
        <span className="font-medium text-gray-900">{destination}</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <div className="flex flex-col items-center">
        <div className="w-3 h-3 rounded-full bg-primary-600 ring-2 ring-primary-200" />
        <div className="w-0.5 h-8 bg-primary-200" />
        <div className="w-3 h-3 rounded-full bg-accent-500 ring-2 ring-accent-200" />
      </div>
      <div className="flex-1">
        <div className="font-semibold text-gray-900">{origin}</div>
        <div className="flex items-center gap-3 my-1 text-xs text-gray-400">
          {distanceKm && <span>{distanceKm} km</span>}
          {durationMinutes && (
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {formatDuration(durationMinutes)}
            </span>
          )}
        </div>
        <div className="font-semibold text-gray-900">{destination}</div>
      </div>
    </div>
  );
}
