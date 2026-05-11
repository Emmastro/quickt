import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Clock, Building2, Bus } from 'lucide-react';
import { t } from '../i18n';
import { useDepartureDetail } from '../hooks/useDepartures';
import { formatXOF, formatDuration, formatTime, formatDate } from '../utils/format';
import RouteDisplay from '../components/common/RouteDisplay';
import SeatMap from '../components/common/SeatMap';
import PriceTag from '../components/common/PriceTag';

export default function DepartureDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: departure, isLoading } = useDepartureDetail(id);
  const [selectedSeats, setSelectedSeats] = useState([]);

  const handleSeatClick = (label) => {
    setSelectedSeats((prev) =>
      prev.includes(label) ? prev.filter((s) => s !== label) : [...prev, label]
    );
  };

  const handleContinue = () => {
    if (selectedSeats.length === 0) return;
    const params = new URLSearchParams({ seats: selectedSeats.join(',') });
    navigate(`/app/book/${id}?${params}`);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  if (!departure) return null;

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      {/* Header */}
      <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      {/* Departure info */}
      <div className="card p-5 mb-4">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
          <Building2 className="w-4 h-4" />
          <span className="font-medium">{departure.agency_name}</span>
          <span className="text-gray-300">|</span>
          <Bus className="w-4 h-4" />
          <span>{departure.bus_model}</span>
        </div>

        <RouteDisplay
          origin={departure.origin_city}
          destination={departure.destination_city}
          distanceKm={departure.distance_km}
          durationMinutes={departure.estimated_duration_minutes}
        />

        <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
          <div>
            <div className="text-xs text-gray-400 uppercase">{t('search.date')}</div>
            <div className="font-medium text-gray-900">{formatDate(departure.departure_date)}</div>
          </div>
          <div>
            <div className="text-xs text-gray-400 uppercase">{t('departure.departure_time')}</div>
            <div className="font-medium text-gray-900">{formatTime(departure.departure_time)}</div>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-400 uppercase">Prix</div>
            <PriceTag amount={departure.price} className="text-lg" />
          </div>
        </div>

        {departure.amenities?.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-100">
            <div className="text-xs text-gray-400 uppercase mb-2">{t('departure.amenities')}</div>
            <div className="flex gap-1.5">
              {departure.amenities.map((a) => (
                <span key={a} className="text-xs bg-primary-50 text-primary-700 px-2.5 py-1 rounded-full font-medium">
                  {a}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Seat selection */}
      <div className="card p-5 mb-4">
        <h2 className="font-semibold text-gray-900 mb-4">{t('departure.select_seats')}</h2>
        <SeatMap
          layout={departure.seat_layout}
          bookedSeats={departure.booked_seats || []}
          selectedSeats={selectedSeats}
          onSeatClick={handleSeatClick}
        />
      </div>

      {/* Selection summary & continue */}
      {selectedSeats.length > 0 && (
        <div className="card p-4 sticky bottom-16 border-2 border-primary-200 bg-white/95 backdrop-blur-sm">
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="text-sm text-gray-500">
                {selectedSeats.length} {selectedSeats.length === 1 ? 'siege' : 'sieges'}: {selectedSeats.join(', ')}
              </div>
              <PriceTag amount={departure.price * selectedSeats.length} className="text-xl" />
            </div>
          </div>
          <button onClick={handleContinue} className="btn-accent w-full">
            {t('departure.continue')}
          </button>
        </div>
      )}
    </div>
  );
}
