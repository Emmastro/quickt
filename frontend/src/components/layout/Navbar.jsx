import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bus, Menu, X } from 'lucide-react';
import { t } from '../../i18n';
import { useAuth } from '../../context/AuthContext';

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { to: '/', label: t('nav.home') },
    { to: '/faq', label: t('nav.faq') },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 bg-primary-700 rounded-xl flex items-center justify-center group-hover:bg-primary-800 transition-colors">
              <Bus className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-primary-800 tracking-tight">
              Quick<span className="text-accent-500">T</span>
            </span>
          </Link>

          {/* Desktop links */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive(to)
                    ? 'text-primary-700 bg-primary-50'
                    : 'text-gray-600 hover:text-primary-700 hover:bg-gray-50'
                }`}
              >
                {label}
              </Link>
            ))}
          </div>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <Link to="/app" className="btn-primary text-sm !px-5 !py-2.5">
                {t('nav.search')}
              </Link>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2.5 text-sm font-medium text-primary-700 hover:bg-primary-50 rounded-lg transition-colors"
                >
                  {t('nav.login')}
                </Link>
                <Link to="/signup" className="btn-accent text-sm !px-5 !py-2.5">
                  {t('nav.signup')}
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden p-2 text-gray-600 hover:text-primary-700"
            aria-label="Menu"
          >
            {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-gray-100 bg-white">
          <div className="px-4 py-3 space-y-1">
            {navLinks.map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                onClick={() => setMobileOpen(false)}
                className={`block px-4 py-2.5 rounded-lg text-sm font-medium ${
                  isActive(to) ? 'text-primary-700 bg-primary-50' : 'text-gray-600'
                }`}
              >
                {label}
              </Link>
            ))}
            <div className="pt-3 border-t border-gray-100 space-y-2">
              {isAuthenticated ? (
                <Link
                  to="/app"
                  onClick={() => setMobileOpen(false)}
                  className="block text-center btn-primary text-sm"
                >
                  {t('nav.search')}
                </Link>
              ) : (
                <>
                  <Link
                    to="/login"
                    onClick={() => setMobileOpen(false)}
                    className="block text-center px-4 py-2.5 text-sm font-medium text-primary-700 bg-primary-50 rounded-lg"
                  >
                    {t('nav.login')}
                  </Link>
                  <Link
                    to="/signup"
                    onClick={() => setMobileOpen(false)}
                    className="block text-center btn-accent text-sm"
                  >
                    {t('nav.signup')}
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
