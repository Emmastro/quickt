import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'sonner';
import QueryProvider from './context/QueryProvider';
import { AuthProvider } from './context/AuthContext';
import RequireAuth from './components/common/RequireAuth';
import Layout from './components/layout/Layout';
import AppLayout from './components/layout/AppLayout';

// Public pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';

// App pages
import SearchPage from './pages/SearchPage';
import ProfilePage from './pages/ProfilePage';
import DepartureDetailPage from './pages/DepartureDetailPage';
import BookingFlowPage from './pages/BookingFlowPage';
import MyTicketsPage from './pages/MyTicketsPage';
import TicketDetailPage from './pages/TicketDetailPage';
import TripPlannerPage from './pages/TripPlannerPage';
import NotificationsPage from './pages/NotificationsPage';

// Agency pages
import AgencyDashboardPage from './pages/agency/AgencyDashboardPage';
import ManageBusesPage from './pages/agency/ManageBusesPage';
import ManageSchedulesPage from './pages/agency/ManageSchedulesPage';
import ManageDeparturesPage from './pages/agency/ManageDeparturesPage';
import PassengerListPage from './pages/agency/PassengerListPage';

// Admin pages
import AdminDashboardPage from './pages/admin/AdminDashboardPage';
import AdminAgenciesPage from './pages/admin/AdminAgenciesPage';
import AdminRoutesPage from './pages/admin/AdminRoutesPage';

export default function App() {
  return (
    <QueryProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public pages with Navbar + Footer */}
            <Route element={<Layout />}>
              <Route index element={<HomePage />} />
              <Route path="home" element={<Navigate to="/" replace />} />
            </Route>

            {/* Auth pages (standalone, no layout) */}
            <Route path="login" element={<LoginPage />} />
            <Route path="signup" element={<SignupPage />} />
            <Route path="forgot-password" element={<ForgotPasswordPage />} />

            {/* Authenticated app shell */}
            <Route
              path="app"
              element={
                <RequireAuth>
                  <AppLayout />
                </RequireAuth>
              }
            >
              <Route index element={<SearchPage />} />
              <Route path="profile" element={<ProfilePage />} />
              <Route path="departures/:id" element={<DepartureDetailPage />} />
              <Route path="book/:departureId" element={<BookingFlowPage />} />
              <Route path="tickets" element={<MyTicketsPage />} />
              <Route path="tickets/:id" element={<TicketDetailPage />} />
              <Route path="trips" element={<TripPlannerPage />} />
              <Route path="notifications" element={<NotificationsPage />} />

              {/* Agency dashboard */}
              <Route path="agency" element={<RequireAuth roles={['agency_staff']}><AgencyDashboardPage /></RequireAuth>} />
              <Route path="agency/buses" element={<RequireAuth roles={['agency_staff']}><ManageBusesPage /></RequireAuth>} />
              <Route path="agency/schedules" element={<RequireAuth roles={['agency_staff']}><ManageSchedulesPage /></RequireAuth>} />
              <Route path="agency/departures" element={<RequireAuth roles={['agency_staff']}><ManageDeparturesPage /></RequireAuth>} />
              <Route path="agency/passengers/:departureId" element={<RequireAuth roles={['agency_staff']}><PassengerListPage /></RequireAuth>} />

              {/* Admin panel */}
              <Route path="admin" element={<RequireAuth roles={['admin']}><AdminDashboardPage /></RequireAuth>} />
              <Route path="admin/agencies" element={<RequireAuth roles={['admin']}><AdminAgenciesPage /></RequireAuth>} />
              <Route path="admin/routes" element={<RequireAuth roles={['admin']}><AdminRoutesPage /></RequireAuth>} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
        <Toaster
          position="top-center"
          toastOptions={{
            className: 'font-sans',
            duration: 4000,
          }}
        />
      </AuthProvider>
    </QueryProvider>
  );
}
