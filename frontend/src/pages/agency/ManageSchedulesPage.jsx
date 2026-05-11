import { useState } from 'react';
import { Plus, X, Zap, Calendar } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { schedulesService } from '../../services/schedules.service';
import { busesService } from '../../services/buses.service';
import { routesService } from '../../services/routes.service';
import { t } from '../../i18n';
import { formatXOF } from '../../utils/format';
import { showToast } from '../../utils/toast';

const DAY_LABELS = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

function formatDays(days) {
  if (!days || days.length === 0) return 'Aucun jour';
  if (days.length === 7) return 'Tous les jours';
  const weekdays = [0, 1, 2, 3, 4];
  const weekend = [5, 6];
  const sorted = [...days].sort();
  if (sorted.length === weekdays.length && sorted.every((d, i) => d === weekdays[i])) return 'Lun–Ven';
  if (sorted.length === weekend.length && sorted.every((d, i) => d === weekend[i])) return 'Sam–Dim';
  return sorted.map((d) => DAY_LABELS[d]).join(', ');
}

export default function ManageSchedulesPage() {
  const queryClient = useQueryClient();
  const { data: schedulesData, isLoading } = useQuery({ queryKey: ['schedules'], queryFn: schedulesService.list });
  const { data: busesData } = useQuery({ queryKey: ['buses'], queryFn: busesService.list });
  const { data: routesData } = useQuery({ queryKey: ['routes'], queryFn: () => routesService.list() });

  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ route_id: '', bus_id: '', departure_time: '08:00', price: 3000, days_of_week: [0, 1, 2, 3, 4, 5, 6] });
  const [genForm, setGenForm] = useState({ schedule_id: null, from_date: '', to_date: '' });

  const createMutation = useMutation({
    mutationFn: schedulesService.create,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['schedules'] }); setShowForm(false); showToast.success('Horaire cree'); },
  });

  const generateMutation = useMutation({
    mutationFn: ({ id, data }) => schedulesService.generateDepartures(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['departures'] });
      showToast.success(`${data.length} depart(s) genere(s)`);
      setGenForm({ schedule_id: null, from_date: '', to_date: '' });
    },
  });

  const schedules = schedulesData?.items || [];
  const buses = busesData?.items || [];
  const routes = routesData?.items || routesData || [];

  const toggleDay = (day) => {
    setForm((prev) => {
      const set = new Set(prev.days_of_week);
      if (set.has(day)) set.delete(day);
      else set.add(day);
      return { ...prev, days_of_week: [...set].sort() };
    });
  };

  const handleCreate = (e) => {
    e.preventDefault();
    if (form.days_of_week.length === 0) {
      showToast.error('Selectionnez au moins un jour de la semaine');
      return;
    }
    createMutation.mutate({ ...form, route_id: Number(form.route_id), bus_id: Number(form.bus_id), price: Number(form.price) });
  };

  const handleGenerate = (e) => {
    e.preventDefault();
    generateMutation.mutate({ id: genForm.schedule_id, data: { from_date: genForm.from_date, to_date: genForm.to_date } });
  };

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-bold text-gray-900">{t('agency.schedules')}</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn-accent !px-4 !py-2 text-sm flex items-center gap-1.5">
          {showForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {showForm ? t('common.close') : 'Ajouter'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card p-5 mb-5 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Itineraire</label>
              <select value={form.route_id} onChange={(e) => setForm({ ...form, route_id: e.target.value })} className="input-field" required>
                <option value="">--</option>
                {routes.map((r) => <option key={r.id} value={r.id}>{r.origin_city} → {r.destination_city}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Bus</label>
              <select value={form.bus_id} onChange={(e) => setForm({ ...form, bus_id: e.target.value })} className="input-field" required>
                <option value="">--</option>
                {buses.map((b) => <option key={b.id} value={b.id}>{b.plate_number} ({b.model})</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Heure de depart</label>
              <input type="time" required value={form.departure_time} onChange={(e) => setForm({ ...form, departure_time: e.target.value })} className="input-field" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Prix (FCFA)</label>
              <input type="number" required min={100} value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} className="input-field" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Jours de circulation</label>
            <div className="flex flex-wrap gap-2">
              {DAY_LABELS.map((label, idx) => {
                const active = form.days_of_week.includes(idx);
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => toggleDay(idx)}
                    className={
                      'px-3 py-1.5 rounded-full text-sm font-medium border transition-colors ' +
                      (active
                        ? 'bg-primary-700 text-white border-primary-700'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-primary-400')
                    }
                  >
                    {label}
                  </button>
                );
              })}
            </div>
            <p className="mt-2 text-xs text-gray-500">L'horaire se repete chaque semaine sur les jours selectionnes.</p>
          </div>
          <button type="submit" className="btn-primary">Creer l'horaire</button>
        </form>
      )}

      {isLoading ? (
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-200 border-t-primary-700" />
        </div>
      ) : schedules.length === 0 ? (
        <div className="card p-8 text-center text-gray-500">Aucun horaire</div>
      ) : (
        <div className="space-y-3">
          {schedules.map((sched) => (
            <div key={sched.id} className="card p-4">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <div className="font-medium text-gray-900">{sched.departure_time?.substring(0, 5)}</div>
                  <div className="text-sm text-gray-500">{formatXOF(sched.price)}</div>
                  <div className="mt-1 flex items-center gap-1 text-xs text-gray-500">
                    <Calendar className="w-3.5 h-3.5" />
                    {formatDays(sched.days_of_week)}
                  </div>
                </div>
                <button
                  onClick={() => setGenForm({ schedule_id: sched.id, from_date: '', to_date: '' })}
                  className="flex items-center gap-1.5 text-sm text-primary-600 font-medium hover:text-primary-800"
                >
                  <Zap className="w-4 h-4" />
                  Generer departs
                </button>
              </div>

              {genForm.schedule_id === sched.id && (
                <form onSubmit={handleGenerate} className="mt-3 pt-3 border-t border-gray-100 space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs text-gray-500 mb-1">Du</label>
                      <input type="date" required value={genForm.from_date} onChange={(e) => setGenForm({ ...genForm, from_date: e.target.value })} className="input-field text-sm" />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-500 mb-1">Au</label>
                      <input type="date" required value={genForm.to_date} onChange={(e) => setGenForm({ ...genForm, to_date: e.target.value })} className="input-field text-sm" />
                    </div>
                  </div>
                  <button type="submit" disabled={generateMutation.isPending} className="btn-primary text-sm !py-2">
                    Generer
                  </button>
                </form>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
