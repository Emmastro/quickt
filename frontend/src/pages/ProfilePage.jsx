import { useState, useEffect } from 'react';
import { LogOut, Globe } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useUpdatePreferences } from '../hooks/useAuth';
import { t } from '../i18n';
import { setLocale, getLocale } from '../i18n';
import { showToast } from '../utils/toast';

const TOGO_CITIES = [
  'Lome', 'Kpalime', 'Atakpame', 'Sokode', 'Kara', 'Dapaong',
  'Tsevie', 'Aneho', 'Bassar', 'Mango', 'Notse', 'Badou',
];

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const updatePrefs = useUpdatePreferences();
  const [form, setForm] = useState({ full_name: '', phone: '', city: '' });
  const [locale, setLocaleState] = useState(getLocale());

  useEffect(() => {
    if (user) {
      setForm({
        full_name: user.full_name || '',
        phone: user.phone || '',
        city: user.city || '',
      });
    }
  }, [user]);

  const updateField = (field) => (e) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await updatePrefs.mutateAsync(form);
      showToast.success(t('common.save'));
    } catch {
      // handled by QueryProvider
    }
  };

  const handleLocaleChange = (e) => {
    const newLocale = e.target.value;
    setLocaleState(newLocale);
    setLocale(newLocale);
    window.location.reload();
  };

  return (
    <div className="px-4 py-6 max-w-lg mx-auto">
      <h1 className="text-xl font-bold text-gray-900 mb-5">{t('profile.title')}</h1>

      {/* User info */}
      <div className="card p-5 mb-4">
        <div className="flex items-center gap-4 mb-5">
          <div className="w-14 h-14 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-xl font-bold">
            {user?.full_name?.charAt(0)?.toUpperCase() || '?'}
          </div>
          <div>
            <div className="font-semibold text-gray-900">{user?.full_name}</div>
            <div className="text-sm text-gray-500">{user?.email}</div>
          </div>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">
              {t('auth.full_name')}
            </label>
            <input
              type="text"
              value={form.full_name}
              onChange={updateField('full_name')}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">
              {t('auth.phone')}
            </label>
            <input
              type="tel"
              value={form.phone}
              onChange={updateField('phone')}
              className="input-field"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">
              {t('auth.city')}
            </label>
            <select value={form.city} onChange={updateField('city')} className="input-field">
              <option value="">--</option>
              {TOGO_CITIES.map((city) => (
                <option key={city} value={city}>{city}</option>
              ))}
            </select>
          </div>
          <button
            type="submit"
            disabled={updatePrefs.isPending}
            className="btn-primary w-full"
          >
            {t('profile.save')}
          </button>
        </form>
      </div>

      {/* Language */}
      <div className="card p-5 mb-4">
        <div className="flex items-center gap-3 mb-3">
          <Globe className="w-5 h-5 text-primary-600" />
          <span className="font-medium text-gray-900">{t('profile.language')}</span>
        </div>
        <select value={locale} onChange={handleLocaleChange} className="input-field">
          <option value="fr">Francais</option>
          <option value="en">English</option>
        </select>
      </div>

      {/* Logout */}
      <button
        onClick={logout}
        className="w-full flex items-center justify-center gap-2 px-4 py-3 text-red-600 bg-red-50 rounded-xl font-medium hover:bg-red-100 transition-colors"
      >
        <LogOut className="w-5 h-5" />
        {t('nav.logout')}
      </button>
    </div>
  );
}
