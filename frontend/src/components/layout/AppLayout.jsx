import { Outlet } from 'react-router-dom';
import AppTopBar from './AppTopBar';
import BottomNav from './BottomNav';
import OfflineBanner from '../common/OfflineBanner';

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <OfflineBanner />
      <AppTopBar />
      <main className="flex-1 pb-16">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
}
