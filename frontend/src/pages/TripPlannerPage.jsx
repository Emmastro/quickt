import { useState } from 'react';
import { Link } from 'react-router-dom';
import { CalendarRange, Plus, Trash2, Search, MapPin, Clock, X } from 'lucide-react';
import { t } from '../i18n';
import { useTrips, useCreateTrip, useDeleteTrip } from '../hooks/useTrips';
import { useRoutes } from '../hooks/useRoutes';
import { formatDate, formatDuration } from '../utils/format';
import RouteDisplay from '../components/common/RouteDisplay';

export default function TripPlannerPage() {
  const { data: trips, isLoading } = useTrips();
  const { data: routesData } = useRoutes();
  const createMutation = useCreateTrip();
  const deleteMutation = useDeleteTrip();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ route_id: '', planned_date: '', notes: '', reminder_hours_before: 24 });

  const routes = routesData?.items || routesData || [];

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await createMutation.mutateAsync({
        ...form,
        route_id: Number(form.route_id),
      });
      setForm({ route_id: '', planned_date: '', notes: '', reminder_hours_before: 24 });
      setShowForm(false);
    } catch { /* handled */ }
  };

  const today = new Date().toISOString().split('T')[0];

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
        <h1 className="text-xl font-bold text-gray-900">{t('trip.planner')}</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-accent !px-4 !py-2 text-sm flex items-center gap-1.5"
        >
          {showForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {showForm ? t('common.close') : t('trip.add')}
        </button>
      </div>

      {/* Create form */}
      {showForm && (
        <form onSubmit={handleCreate} className="card p-5 mb-5 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">{t('trip.route')}</label>
            <select
              value={form.route_id}
              onChange={(e) => setForm({ ...form, route_id: e.target.value })}
              className="input-field"
              required
            >
              <option value="">--</option>
              {routes.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.origin_city} → {r.destination_city}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">{t('trip.date')}</label>
            <input
              type="date"
              min={today}
              value={form.planned_date}
              onChange={(e) => setForm({ ...form, planned_date: e.target.value })}
              className="input-field"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">{t('trip.notes')}</label>
            <textarea
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              className="input-field"
              rows={2}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">{t('trip.reminder')}</label>
            <select
              value={form.reminder_hours_before}
              onChange={(e) => setForm({ ...form, reminder_hours_before: Number(e.target.value) })}
              className="input-field"
            >
              <option value={6}>6h</option>
              <option value={12}>12h</option>
              <option value={24}>24h</option>
              <option value={48}>48h</option>
            </select>
          </div>
          <button type="submit" disabled={createMutation.isPending} className="btn-primary w-full">
            {t('common.save')}
          </button>
        </form>
      )}

      {/* Trip list */}
      {(!trips || trips.length === 0) ? (
        <div className="card p-8 text-center">
          <CalendarRange className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">{t('trip.no_trips')}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {trips.map((trip) => (
            <div key={trip.id} className="card p-4">
              <div className="flex items-start justify-between mb-3">
                <RouteDisplay
                  origin={trip.origin_city}
                  destination={trip.destination_city}
                  distanceKm={trip.distance_km}
                  durationMinutes={trip.estimated_duration_minutes}
                />
                <button
                  onClick={() => deleteMutation.mutate(trip.id)}
                  className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                <span className="flex items-center gap-1">
                  <CalendarRange className="w-4 h-4" />
                  {formatDate(trip.planned_date)}
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  Rappel: {trip.reminder_hours_before}h
                </span>
              </div>

              {trip.notes && (
                <p className="text-sm text-gray-400 mb-3 italic">{trip.notes}</p>
              )}

              <Link
                to={`/app?origin=${encodeURIComponent(trip.origin_city)}&destination=${encodeURIComponent(trip.destination_city)}&date=${trip.planned_date}`}
                className="inline-flex items-center gap-1.5 text-sm text-primary-600 font-medium hover:text-primary-800"
              >
                <Search className="w-4 h-4" />
                {t('trip.search_departures')}
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
