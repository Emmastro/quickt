import { useState } from 'react';
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Check, CreditCard, QrCode } from 'lucide-react';
import { t } from '../i18n';
import { useDepartureDetail } from '../hooks/useDepartures';
import { useReserveTickets } from '../hooks/useTickets';
import { useInitiatePayment } from '../hooks/usePayments';
import { formatXOF, formatTime, formatDate } from '../utils/format';
import RouteDisplay from '../components/common/RouteDisplay';
import PriceTag from '../components/common/PriceTag';
import { showToast } from '../utils/toast';

const STEPS = ['seats', 'passengers', 'payment', 'confirmation'];

export default function BookingFlowPage() {
  const { departureId } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const seats = (searchParams.get('seats') || '').split(',').filter(Boolean);

  const { data: departure } = useDepartureDetail(departureId);
  const reserveMutation = useReserveTickets();
  const paymentMutation = useInitiatePayment();

  const [step, setStep] = useState(0);
  const [passengers, setPassengers] = useState(
    seats.map((seat) => ({ seat_number: seat, passenger_name: '', passenger_phone: '' }))
  );
  const [bookingResult, setBookingResult] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('flooz');
  const [paymentPhone, setPaymentPhone] = useState('');

  const updatePassenger = (index, field, value) => {
    setPassengers((prev) => {
      const copy = [...prev];
      copy[index] = { ...copy[index], [field]: value };
      return copy;
    });
  };

  const allPassengersFilled = passengers.every(
    (p) => p.passenger_name.trim() && p.passenger_phone.trim()
  );

  const handlePayment = async () => {
    try {
      // Step 1: Reserve tickets
      const reservation = await reserveMutation.mutateAsync({
        departure_id: Number(departureId),
        seats: passengers,
      });

      // Step 2: Initiate payment
      await paymentMutation.mutateAsync({
        booking_reference: reservation.booking_reference,
        method: paymentMethod,
        phone: paymentPhone || passengers[0].passenger_phone,
      });

      // Payment auto-confirms in sandbox mode, so tickets are now confirmed
      setBookingResult(reservation);
      setStep(3);
      showToast.success(t('toast.booking_success'));
    } catch {
      // Handled by QueryProvider
    }
  };

  if (!departure) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary-200 border-t-primary-700" />
      </div>
    );
  }

  const totalPrice = departure.price * seats.length;

  return (
    <div className="px-4 py-6 max-w-2xl mx-auto">
      {/* Header */}
      <button
        onClick={() => (step > 0 && step < 3 ? setStep(step - 1) : navigate(-1))}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        {t('common.back')}
      </button>

      <h1 className="text-xl font-bold text-gray-900 mb-4">{t('booking.title')}</h1>

      {/* Step indicator */}
      <div className="flex items-center gap-1 mb-6">
        {STEPS.map((s, i) => (
          <div key={s} className="flex-1 flex items-center">
            <div
              className={`w-full h-1.5 rounded-full ${
                i <= step ? 'bg-primary-600' : 'bg-gray-200'
              }`}
            />
          </div>
        ))}
      </div>

      {/* Trip summary */}
      {step < 3 && (
        <div className="card p-4 mb-4">
          <RouteDisplay
            origin={departure.origin_city}
            destination={departure.destination_city}
            compact
          />
          <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
            <span>{formatDate(departure.departure_date)}</span>
            <span>{formatTime(departure.departure_time)}</span>
          </div>
        </div>
      )}

      {/* Step 0: Confirm seats */}
      {step === 0 && (
        <div>
          <div className="card p-5 mb-4">
            <h2 className="font-semibold text-gray-900 mb-3">{t('booking.step.seats')}</h2>
            <div className="space-y-2">
              {seats.map((seat) => (
                <div key={seat} className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded-lg">
                  <span className="font-medium">{t('ticket.seat')}: {seat}</span>
                  <PriceTag amount={departure.price} />
                </div>
              ))}
            </div>
            <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-200">
              <span className="font-semibold">{t('booking.total')}</span>
              <PriceTag amount={totalPrice} className="text-xl" />
            </div>
          </div>
          <button onClick={() => setStep(1)} className="btn-primary w-full">
            {t('common.next')}
          </button>
        </div>
      )}

      {/* Step 1: Passenger details */}
      {step === 1 && (
        <div>
          <div className="space-y-4 mb-4">
            {passengers.map((p, i) => (
              <div key={p.seat_number} className="card p-5">
                <div className="text-sm font-medium text-primary-600 mb-3">
                  {t('ticket.seat')}: {p.seat_number}
                </div>
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {t('booking.passenger_name')}
                    </label>
                    <input
                      type="text"
                      required
                      value={p.passenger_name}
                      onChange={(e) => updatePassenger(i, 'passenger_name', e.target.value)}
                      className="input-field"
                      placeholder="Kofi Mensah"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      {t('booking.passenger_phone')}
                    </label>
                    <input
                      type="tel"
                      required
                      value={p.passenger_phone}
                      onChange={(e) => updatePassenger(i, 'passenger_phone', e.target.value)}
                      className="input-field"
                      placeholder="+228 90 00 00 00"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
          <button
            onClick={() => setStep(2)}
            disabled={!allPassengersFilled}
            className="btn-primary w-full"
          >
            {t('common.next')}
          </button>
        </div>
      )}

      {/* Step 2: Payment */}
      {step === 2 && (
        <div>
          <div className="card p-5 mb-4">
            <h2 className="font-semibold text-gray-900 mb-4">{t('booking.select_payment')}</h2>

            <div className="space-y-3 mb-4">
              <label
                className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-colors ${
                  paymentMethod === 'flooz'
                    ? 'border-2 border-primary-200 bg-primary-50'
                    : 'border border-gray-200 hover:border-primary-200'
                }`}
              >
                <input
                  type="radio"
                  name="payment"
                  checked={paymentMethod === 'flooz'}
                  onChange={() => setPaymentMethod('flooz')}
                  className="text-primary-600"
                />
                <CreditCard className={`w-5 h-5 ${paymentMethod === 'flooz' ? 'text-primary-600' : 'text-gray-400'}`} />
                <span className="font-medium text-gray-900">Flooz</span>
              </label>
              <label
                className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition-colors ${
                  paymentMethod === 't_money'
                    ? 'border-2 border-primary-200 bg-primary-50'
                    : 'border border-gray-200 hover:border-primary-200'
                }`}
              >
                <input
                  type="radio"
                  name="payment"
                  checked={paymentMethod === 't_money'}
                  onChange={() => setPaymentMethod('t_money')}
                  className="text-primary-600"
                />
                <CreditCard className={`w-5 h-5 ${paymentMethod === 't_money' ? 'text-primary-600' : 'text-gray-400'}`} />
                <span className="font-medium text-gray-900">T-Money</span>
              </label>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t('booking.phone_number')}
              </label>
              <input
                type="tel"
                value={paymentPhone}
                onChange={(e) => setPaymentPhone(e.target.value)}
                className="input-field"
                placeholder="+228 90 00 00 00"
              />
            </div>

            <div className="flex items-center justify-between py-3 border-t border-gray-200">
              <span className="font-semibold">{t('booking.total')}</span>
              <PriceTag amount={totalPrice} className="text-xl" />
            </div>
          </div>

          <button
            onClick={handlePayment}
            disabled={reserveMutation.isPending || paymentMutation.isPending}
            className="btn-accent w-full flex items-center justify-center gap-2"
          >
            {(reserveMutation.isPending || paymentMutation.isPending) ? (
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white/30 border-t-white" />
            ) : (
              <>
                <CreditCard className="w-5 h-5" />
                {t('booking.pay_now')} — {formatXOF(totalPrice)}
              </>
            )}
          </button>
        </div>
      )}

      {/* Step 3: Confirmation */}
      {step === 3 && bookingResult && (
        <div className="text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Check className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">{t('booking.success')}</h2>
          <p className="text-gray-500 mb-6">{t('booking.success_desc')}</p>

          <div className="card p-4 mb-4 text-left">
            <div className="text-sm text-gray-500 mb-1">Ref:</div>
            <div className="text-lg font-bold text-primary-700 font-mono mb-4">
              {bookingResult.booking_reference}
            </div>

            <div className="space-y-3">
              {bookingResult.tickets.map((ticket) => (
                <div key={ticket.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
                  <div>
                    <div className="font-medium">{ticket.seat_number}</div>
                    <div className="text-xs text-gray-500 font-mono">{ticket.code}</div>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <QrCode className="w-4 h-4" />
                    <span>{t('ticket.show_qr')}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => navigate('/app/tickets')}
              className="btn-primary flex-1"
            >
              {t('ticket.my_tickets')}
            </button>
            <button
              onClick={() => navigate('/app')}
              className="btn-secondary flex-1"
            >
              {t('nav.search')}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
