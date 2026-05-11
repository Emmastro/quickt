import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bus, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { t } from '../i18n';

const TOGO_CITIES = [
  'Lome', 'Kpalime', 'Atakpame', 'Sokode', 'Kara', 'Dapaong',
  'Tsevie', 'Aneho', 'Bassar', 'Mango', 'Notse', 'Badou',
];

export default function SignupPage() {
  const [form, setForm] = useState({
    full_name: '',
    email: '',
    phone: '',
    city: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const { register, isRegisterPending } = useAuth();
  const navigate = useNavigate();

  const updateField = (field) => (e) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(form);
      navigate('/app', { replace: true });
    } catch {
      // Error handled by mutation's onError in QueryProvider
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-primary-50 via-white to-primary-50 px-4 py-12">
      {/* Logo */}
      <Link to="/" className="flex items-center gap-2.5 mb-8">
        <div className="w-11 h-11 bg-primary-700 rounded-xl flex items-center justify-center">
          <Bus className="w-6 h-6 text-white" />
        </div>
        <span className="text-2xl font-bold text-primary-800 tracking-tight">
          Quick<span className="text-accent-500">T</span>
        </span>
      </Link>

      {/* Card */}
      <div className="w-full max-w-md">
        <div className="card p-8">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-1">
              {t('auth.signup_title')}
            </h1>
            <p className="text-sm text-gray-500">{t('auth.signup_subtitle')}</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.full_name')}
              </label>
              <input
                id="full_name"
                type="text"
                required
                value={form.full_name}
                onChange={updateField('full_name')}
                className="input-field"
                placeholder="Kofi Mensah"
                autoComplete="name"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.email')}
              </label>
              <input
                id="email"
                type="email"
                required
                value={form.email}
                onChange={updateField('email')}
                className="input-field"
                placeholder="vous@exemple.com"
                autoComplete="email"
              />
            </div>

            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.phone')}
              </label>
              <input
                id="phone"
                type="tel"
                required
                value={form.phone}
                onChange={updateField('phone')}
                className="input-field"
                placeholder="+228 90 00 00 00"
                autoComplete="tel"
              />
            </div>

            <div>
              <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.city')}
              </label>
              <select
                id="city"
                value={form.city}
                onChange={updateField('city')}
                className="input-field"
              >
                <option value="">--</option>
                {TOGO_CITIES.map((city) => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.password')}
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  minLength={8}
                  value={form.password}
                  onChange={updateField('password')}
                  className="input-field !pr-11"
                  placeholder="********"
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={isRegisterPending}
              className="btn-primary w-full flex items-center justify-center"
            >
              {isRegisterPending ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
              ) : (
                t('auth.signup_btn')
              )}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            {t('auth.has_account')}{' '}
            <Link to="/login" className="font-medium text-primary-600 hover:text-primary-800">
              {t('auth.login_link')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
