import { useState } from 'react';
import { Plus, Edit2, Trash2, X } from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { busesService } from '../../services/buses.service';
import { t } from '../../i18n';
import { showToast } from '../../utils/toast';

export default function ManageBusesPage() {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({ queryKey: ['buses'], queryFn: busesService.list });
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState({ plate_number: '', model: '', capacity: 30 });

  const createMutation = useMutation({
    mutationFn: busesService.create,
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['buses'] }); resetForm(); showToast.success('Bus cree'); },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => busesService.update(id, data),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['buses'] }); resetForm(); },
  });

  const deleteMutation = useMutation({
    mutationFn: busesService.delete,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['buses'] }),
  });

  const resetForm = () => {
    setForm({ plate_number: '', model: '', capacity: 30 });
    setShowForm(false);
    setEditId(null);
  };

  const handleEdit = (bus) => {
    setForm({ plate_number: bus.plate_number, model: bus.model, capacity: bus.capacity });
    setEditId(bus.id);
    setShowForm(true);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (editId) {
      updateMutation.mutate({ id: editId, data: form });
    } else {
      createMutation.mutate(form);
    }
  };

  const buses = data?.items || [];

  return (
    <div className="px-4 py-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-5">
        <h1 className="text-xl font-bold text-gray-900">{t('agency.buses')}</h1>
        <button onClick={() => { resetForm(); setShowForm(!showForm); }} className="btn-accent !px-4 !py-2 text-sm flex items-center gap-1.5">
          {showForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {showForm ? t('common.close') : 'Ajouter'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card p-5 mb-5 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Immatriculation</label>
              <input type="text" required value={form.plate_number} onChange={(e) => setForm({ ...form, plate_number: e.target.value })} className="input-field" placeholder="TG-1234-AB" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Modele</label>
              <input type="text" required value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })} className="input-field" placeholder="Mercedes Sprinter" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Capacite</label>
              <input type="number" required min={1} value={form.capacity} onChange={(e) => setForm({ ...form, capacity: Number(e.target.value) })} className="input-field" />
            </div>
          </div>
          <button type="submit" className="btn-primary">{editId ? t('common.save') : 'Ajouter'}</button>
        </form>
      )}

      {isLoading ? (
        <div className="flex justify-center py-10">
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary-200 border-t-primary-700" />
        </div>
      ) : buses.length === 0 ? (
        <div className="card p-8 text-center text-gray-500">Aucun bus</div>
      ) : (
        <div className="space-y-2">
          {buses.map((bus) => (
            <div key={bus.id} className="card p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900">{bus.plate_number}</div>
                <div className="text-sm text-gray-500">{bus.model} — {bus.capacity} places</div>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => handleEdit(bus)} className="p-2 text-gray-400 hover:text-primary-600"><Edit2 className="w-4 h-4" /></button>
                <button onClick={() => deleteMutation.mutate(bus.id)} className="p-2 text-gray-400 hover:text-red-500"><Trash2 className="w-4 h-4" /></button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
