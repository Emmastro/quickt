import { Link } from 'react-router-dom';
import { Bus, Mail, Phone, MapPin } from 'lucide-react';
import { t } from '../../i18n';

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-primary-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 bg-accent-500 rounded-xl flex items-center justify-center">
                <Bus className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold tracking-tight">
                Quick<span className="text-accent-400">T</span>
              </span>
            </Link>
            <p className="text-primary-200 text-sm leading-relaxed max-w-md">
              {t('footer.description')}
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-semibold text-sm uppercase tracking-wider text-primary-300 mb-4">
              Navigation
            </h4>
            <ul className="space-y-2.5">
              <li>
                <Link to="/" className="text-sm text-primary-200 hover:text-white transition-colors">
                  {t('nav.home')}
                </Link>
              </li>
              <li>
                <Link to="/faq" className="text-sm text-primary-200 hover:text-white transition-colors">
                  {t('nav.faq')}
                </Link>
              </li>
              <li>
                <Link to="/login" className="text-sm text-primary-200 hover:text-white transition-colors">
                  {t('nav.login')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-semibold text-sm uppercase tracking-wider text-primary-300 mb-4">
              {t('footer.contact')}
            </h4>
            <ul className="space-y-2.5">
              <li className="flex items-center gap-2 text-sm text-primary-200">
                <Mail className="w-4 h-4 text-accent-400" />
                contact@quickt.tg
              </li>
              <li className="flex items-center gap-2 text-sm text-primary-200">
                <Phone className="w-4 h-4 text-accent-400" />
                +228 90 00 00 00
              </li>
              <li className="flex items-center gap-2 text-sm text-primary-200">
                <MapPin className="w-4 h-4 text-accent-400" />
                Lome, Togo
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-10 pt-6 border-t border-primary-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-primary-400">
            &copy; {year} {t('footer.copyright')}
          </p>
          <div className="flex items-center gap-4">
            <Link to="/legal" className="text-xs text-primary-400 hover:text-white transition-colors">
              {t('footer.legal')}
            </Link>
            <Link to="/privacy" className="text-xs text-primary-400 hover:text-white transition-colors">
              {t('footer.privacy')}
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
