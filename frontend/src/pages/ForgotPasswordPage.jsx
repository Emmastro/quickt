import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Bus, ArrowLeft, CheckCircle } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';
import { authService } from '../services/auth.service';
import { t } from '../i18n';
import { showToast } from '../utils/toast';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  const mutation = useMutation({
    mutationFn: () => authService.forgotPassword(email),
    onSuccess: () => setSent(true),
    onError: () => {
      // For security, show success even on error (don't reveal if email exists)
      setSent(true);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate();
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

      <div className="w-full max-w-md">
        <div className="card p-8">
          {sent ? (
            <div className="text-center py-4">
              <div className="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-7 h-7 text-green-600" />
              </div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Email envoye</h2>
              <p className="text-sm text-gray-500 mb-6">
                Si un compte existe avec l'adresse <strong>{email}</strong>, vous recevrez un lien de reinitialisation.
              </p>
              <Link to="/login" className="btn-primary inline-flex items-center gap-2">
                <ArrowLeft className="w-4 h-4" />
                {t('auth.back_to_login')}
              </Link>
            </div>
          ) : (
            <>
              <div className="text-center mb-8">
                <h1 className="text-2xl font-bold text-gray-900 mb-1">
                  {t('auth.forgot_title')}
                </h1>
                <p className="text-sm text-gray-500">{t('auth.forgot_subtitle')}</p>
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

                <button
                  type="submit"
                  disabled={mutation.isPending}
                  className="btn-primary w-full flex items-center justify-center"
                >
                  {mutation.isPending ? (
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
                  ) : (
                    t('auth.send_reset')
                  )}
                </button>
              </form>

              <p className="mt-6 text-center">
                <Link to="/login" className="text-sm font-medium text-primary-600 hover:text-primary-800 flex items-center justify-center gap-1">
                  <ArrowLeft className="w-4 h-4" />
                  {t('auth.back_to_login')}
                </Link>
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
