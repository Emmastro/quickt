import { useState } from 'react';
import { Plus, X } from 'lucide-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useRoutes } from '../../hooks/useRoutes';
import { routesService } from '../../services/routes.service';
import { t } from '../../i18n';
import { formatDuration } from '../../utils/format';
import { showToast } from '../../utils/toast';

export default function AdminRoutesPage() {
  const queryClient = useQueryClient();
  const { data, isLoading } = useRoutes();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ origin_city: '', destination_city: '', distance_km: '', estimated_duration_minutes: '' });

  const createMutation = useMutation({
    mutationFn: routesService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['routes'] });
      setShowForm(false);
      setForm({ origin_city: '', destination_city: '', distance_km: '', estimated_duration_minutes: '' });
      showToast.success('Itineraire cree');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate({
      ...form,
      distance_km: Number(form.distance_km),
      estimated_duration_minutes: Number(form.estimated_duration_minutes),
    });
  };

  const routes = data?.items || data || [];

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-bold text-gray-900">{t('admin.routes')}</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn-accent !px-4 !py-2 text-sm flex items-center gap-1.5">
          {showForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {showForm ? t('common.close') : 'Ajouter'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card p-5 mb-5 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Origine</label>
              <input type="text" required value={form.origin_city} onChange={(e) => setForm({ ...form, origin_city: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
              <input type="text" required value={form.destination_city} onChange={(e) => setForm({ ...form, destination_city: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Distance (km)</label>
              <input type="number" required min={1} value={form.distance_km} onChange={(e) => setForm({ ...form, distance_km: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Duree (minutes)</label>
              <input type="number" required min={1} value={form.estimated_duration_minutes} onChange={(e) => setForm({ ...form, estimated_duration_minutes: e.target.value })} className="input-field" />
            </div>
          </div>
          <button type="submit" className="btn-primary">Creer</button>
        </form>
      )}

      {isLoading ? (
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-200 border-t-primary-700" />
        </div>
      ) : (
        <div className="space-y-2">
          {routes.map((route) => (
            <div key={route.id} className="card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">{route.origin_city} → {route.destination_city}</div>
                <div className="text-sm text-gray-500">
                  {route.distance_km} km — {formatDuration(route.estimated_duration_minutes)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
