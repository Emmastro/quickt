import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Bus, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { t } from '../i18n';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login, isLoginPending } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/app';

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login({ email, password });
      navigate(from, { replace: true });
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
              {t('auth.login_title')}
            </h1>
            <p className="text-sm text-gray-500">{t('auth.login_subtitle')}</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.email')}
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field"
                placeholder="vous@exemple.com"
                autoComplete="email"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  {t('auth.password')}
                </label>
                <Link to="/forgot-password" className="text-xs text-primary-600 hover:text-primary-800">
                  {t('auth.forgot_password')}
                </Link>
              </div>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-field !pr-11"
                  placeholder="********"
                  autoComplete="current-password"
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
              disabled={isLoginPending}
              className="btn-primary w-full flex items-center justify-center"
            >
              {isLoginPending ? (
                <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
              ) : (
                t('auth.login_btn')
              )}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            {t('auth.no_account')}{' '}
            <Link to="/signup" className="font-medium text-primary-600 hover:text-primary-800">
              {t('auth.signup_link')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
