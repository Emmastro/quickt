import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from '../../context/AuthContext';
import { setActiveMessages } from '../../i18n';
import LoginPage from '../LoginPage';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

function renderWithProviders(ui) {
  return render(
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <MemoryRouter>{ui}</MemoryRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

beforeAll(() => {
  setActiveMessages({
    'auth.login_title': 'Connexion',
    'auth.login_subtitle': 'Accedez a votre compte QuickT',
    'auth.email': 'Email',
    'auth.password': 'Mot de passe',
    'auth.login_btn': 'Se connecter',
    'auth.no_account': 'Pas de compte?',
    'auth.signup_link': 'Inscrivez-vous',
    'auth.forgot_password': 'Mot de passe oublie?',
    'common.loading': 'Chargement...',
  });
});

describe('LoginPage', () => {
  it('renders the login form', () => {
    renderWithProviders(<LoginPage />);
    expect(screen.getByText('Connexion')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Mot de passe')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Se connecter' })).toBeInTheDocument();
  });

  it('has a link to signup page', () => {
    renderWithProviders(<LoginPage />);
    expect(screen.getByText('Inscrivez-vous')).toBeInTheDocument();
  });

  it('has a forgot password link', () => {
    renderWithProviders(<LoginPage />);
    expect(screen.getByText('Mot de passe oublie?')).toBeInTheDocument();
  });
});
