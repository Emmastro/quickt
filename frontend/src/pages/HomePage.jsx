import { Link } from 'react-router-dom';
import { Search, MapPin, CreditCard, QrCode, ArrowRight, Clock, Users, Bus } from 'lucide-react';
import { t } from '../i18n';
import { usePopularRoutes } from '../hooks/useRoutes';
import { formatXOF, formatDuration } from '../utils/format';

const STEPS = [
  { icon: Search, color: 'bg-blue-100 text-blue-700', key: 'step1' },
  { icon: MapPin, color: 'bg-indigo-100 text-indigo-700', key: 'step2' },
  { icon: CreditCard, color: 'bg-amber-100 text-amber-700', key: 'step3' },
  { icon: QrCode, color: 'bg-green-100 text-green-700', key: 'step4' },
];

export default function HomePage() {
  const { data: popularRoutes } = usePopularRoutes();

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-800 via-primary-700 to-primary-900">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 rounded-full bg-accent-400 blur-3xl" />
          <div className="absolute bottom-10 right-10 w-96 h-96 rounded-full bg-primary-400 blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-1.5 mb-6">
              <Bus className="w-4 h-4 text-accent-400" />
              <span className="text-sm text-white/90 font-medium">{t('app.tagline')}</span>
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-white leading-tight mb-6">
              {t('home.hero.title')}
              <span className="text-accent-400">.</span>
            </h1>

            <p className="text-lg md:text-xl text-primary-100 leading-relaxed mb-8 max-w-lg">
              {t('home.hero.subtitle')}
            </p>

            <div className="flex flex-col sm:flex-row gap-3">
              <Link to="/app" className="btn-accent text-center !px-8 !py-4 text-lg flex items-center justify-center gap-2">
                {t('home.hero.search_btn')}
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link to="/signup" className="btn-secondary text-center !px-8 !py-4 text-lg !bg-white/10 !text-white !border-white/20 hover:!bg-white/20">
                {t('nav.signup')}
              </Link>
            </div>
          </div>
        </div>

        {/* Wave separator */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 60" fill="none" className="w-full h-auto">
            <path d="M0 60V30C240 0 480 0 720 30C960 60 1200 60 1440 30V60H0Z" fill="#f9fafb" />
          </svg>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 md:py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
              {t('home.how.title')}
            </h2>
            <div className="w-16 h-1 bg-accent-500 rounded-full mx-auto" />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {STEPS.map(({ icon: Icon, color, key }, index) => (
              <div key={key} className="card p-6 text-center hover:shadow-md transition-shadow group">
                <div className="relative mb-5">
                  <div className={`w-14 h-14 ${color} rounded-2xl flex items-center justify-center mx-auto group-hover:scale-110 transition-transform`}>
                    <Icon className="w-7 h-7" />
                  </div>
                  <span className="absolute -top-2 -right-2 w-7 h-7 bg-primary-700 text-white text-xs font-bold rounded-full flex items-center justify-center">
                    {index + 1}
                  </span>
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  {t(`home.how.${key}.title`)}
                </h3>
                <p className="text-sm text-gray-500 leading-relaxed">
                  {t(`home.how.${key}.desc`)}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Popular routes */}
      {popularRoutes?.length > 0 && (
        <section className="py-16 md:py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
                {t('home.popular.title')}
              </h2>
              <div className="w-16 h-1 bg-accent-500 rounded-full mx-auto" />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {popularRoutes.map((route) => (
                <Link
                  key={route.id}
                  to={`/app?origin=${encodeURIComponent(route.origin_city)}&destination=${encodeURIComponent(route.destination_city)}`}
                  className="card p-5 hover:shadow-lg transition-all group border-l-4 border-l-primary-600"
                >
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 bg-primary-50 rounded-xl flex items-center justify-center">
                      <MapPin className="w-5 h-5 text-primary-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-gray-900 group-hover:text-primary-700 transition-colors">
                        {route.origin_city}
                      </div>
                      <div className="text-xs text-gray-400 flex items-center gap-1">
                        <ArrowRight className="w-3 h-3" />
                        {route.destination_city}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    {route.distance_km && (
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3 h-3" />
                        {route.distance_km} km
                      </span>
                    )}
                    {route.estimated_duration_minutes && (
                      <span className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {formatDuration(route.estimated_duration_minutes)}
                      </span>
                    )}
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="py-16 md:py-20 bg-gradient-to-r from-primary-700 to-primary-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            {t('home.cta.title')}
          </h2>
          <p className="text-lg text-primary-100 mb-8 max-w-xl mx-auto">
            {t('home.cta.subtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link to="/signup" className="btn-accent text-center !px-8 !py-4 text-lg">
              {t('nav.signup')}
            </Link>
            <Link to="/app" className="btn-secondary text-center !px-8 !py-4 text-lg !bg-white/10 !text-white !border-white/20 hover:!bg-white/20">
              {t('home.hero.search_btn')}
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
