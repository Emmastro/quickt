import { useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Search, ArrowRightLeft, Clock, Users, Building2 } from 'lucide-react';
import { t } from '../i18n';
import { useSearchDepartures } from '../hooks/useDepartures';
import { formatXOF, formatDuration, formatTime } from '../utils/format';
import RouteDisplay from '../components/common/RouteDisplay';

const TOGO_CITIES = [
  'Lome', 'Kpalime', 'Atakpame', 'Sokode', 'Kara', 'Dapaong',
  'Tsevie', 'Aneho', 'Bassar', 'Mango', 'Notse', 'Badou',
];

export default function SearchPage() {
  const [searchParams] = useSearchParams();
  const [origin, setOrigin] = useState(searchParams.get('origin') || '');
  const [destination, setDestination] = useState(searchParams.get('destination') || '');
  const [date, setDate] = useState(searchParams.get('date') || '');
  const [searchTriggered, setSearchTriggered] = useState(false);
  const [searchQuery, setSearchQuery] = useState(null);

  const { data: results, isLoading } = useSearchDepartures(searchQuery);

  const swapCities = () => {
    setOrigin(destination);
    setDestination(origin);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (origin && destination && date) {
      setSearchQuery({ origin, destination, date });
      setSearchTriggered(true);
    }
  };

  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">
        {t('search.title')}
      </h1>

      <form onSubmit={handleSearch} className="card p-5 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">
            {t('search.origin')}
          </label>
          <select value={origin} onChange={(e) => setOrigin(e.target.value)} className="input-field">
            <option value="">--</option>
            {TOGO_CITIES.filter((c) => c !== destination).map((city) => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        <div className="flex justify-center">
          <button
            type="button"
            onClick={swapCities}
            className="p-2.5 bg-primary-50 text-primary-700 rounded-full hover:bg-primary-100 transition-colors"
            title={t('search.swap')}
          >
            <ArrowRightLeft className="w-5 h-5" />
          </button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">
            {t('search.destination')}
          </label>
          <select value={destination} onChange={(e) => setDestination(e.target.value)} className="input-field">
            <option value="">--</option>
            {TOGO_CITIES.filter((c) => c !== origin).map((city) => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">
            {t('search.date')}
          </label>
          <input
            type="date"
            value={date}
            min={today}
            onChange={(e) => setDate(e.target.value)}
            className="input-field"
          />
        </div>

        <button
          type="submit"
          disabled={!origin || !destination || !date || isLoading}
          className="btn-accent w-full flex items-center justify-center gap-2 !mt-6"
        >
          {isLoading ? (
            <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
          ) : (
            <>
              <Search className="w-5 h-5" />
              {t('search.btn')}
            </>
          )}
        </button>
      </form>

      {/* Results */}
      {searchTriggered && (
        <div className="mt-6 space-y-3">
          {results?.length > 0 && (
            <p className="text-sm text-gray-500">
              {t('search.results_count', { values: { count: results.length } })}
            </p>
          )}

          {results?.length === 0 && !isLoading && (
            <div className="card p-8 text-center">
              <p className="text-gray-500">{t('search.no_results')}</p>
            </div>
          )}

          {results?.map((dep) => (
            <Link
              key={dep.id}
              to={`/app/departures/${dep.id}`}
              className="card p-4 block hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <Building2 className="w-3.5 h-3.5" />
                  <span className="font-medium">{dep.agency_name}</span>
                </div>
                <span className="text-lg font-bold text-primary-700">
                  {formatXOF(dep.price)}
                </span>
              </div>

              <RouteDisplay
                origin={dep.origin_city}
                destination={dep.destination_city}
                distanceKm={dep.distance_km}
                durationMinutes={dep.estimated_duration_minutes}
              />

              <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                <div className="flex items-center gap-1.5 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span className="font-medium">{formatTime(dep.departure_time)}</span>
                </div>
                <div className="flex items-center gap-1.5 text-sm">
                  <Users className="w-4 h-4 text-green-600" />
                  <span className="text-green-700 font-medium">
                    {t('departure.seats_available', { values: { count: dep.available_seats } })}
                  </span>
                </div>
              </div>

              {dep.amenities?.length > 0 && (
                <div className="flex gap-1.5 mt-2">
                  {dep.amenities.map((a) => (
                    <span key={a} className="text-[10px] bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full font-medium">
                      {a}
                    </span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
