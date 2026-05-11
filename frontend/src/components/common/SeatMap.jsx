import { t } from '../../i18n';

function generateSeatLabels(layout) {
  const { rows, seats_per_row, labels, unavailable_seats = [] } = layout;
  if (labels?.length) return labels;

  const generated = [];
  const cols = 'ABCDEFGHIJ'.slice(0, seats_per_row);
  for (let r = 1; r <= rows; r++) {
    for (const col of cols) {
      const label = `${r}${col}`;
      if (!unavailable_seats.includes(label)) {
        generated.push(label);
      }
    }
  }
  return generated;
}

export default function SeatMap({
  layout,
  bookedSeats = [],
  selectedSeats = [],
  onSeatClick,
  maxSelectable = 10,
}) {
  const { rows, seats_per_row, aisle_after_column = 2 } = layout;
  const cols = 'ABCDEFGHIJ'.slice(0, seats_per_row);
  const unavailable = new Set(layout.unavailable_seats || []);

  const getSeatState = (label) => {
    if (bookedSeats.includes(label)) return 'taken';
    if (selectedSeats.includes(label)) return 'selected';
    if (unavailable.has(label)) return 'unavailable';
    return 'available';
  };

  const handleClick = (label) => {
    const state = getSeatState(label);
    if (state === 'taken' || state === 'unavailable') return;
    if (state === 'available' && selectedSeats.length >= maxSelectable) return;
    onSeatClick?.(label);
  };

  return (
    <div>
      {/* Bus front indicator */}
      <div className="text-center text-xs text-gray-400 mb-3 font-medium uppercase tracking-wider">
        Avant du bus
      </div>

      {/* Seat grid */}
      <div className="flex flex-col items-center gap-1.5">
        {Array.from({ length: rows }, (_, r) => (
          <div key={r} className="flex items-center gap-1.5">
            {cols.split('').map((col, colIdx) => {
              const label = `${r + 1}${col}`;
              const state = getSeatState(label);
              const isUnavailable = state === 'unavailable';

              return (
                <div key={col} className="contents">
                  <button
                    type="button"
                    disabled={isUnavailable}
                    onClick={() => handleClick(label)}
                    className={`seat ${
                      state === 'taken'
                        ? 'seat-taken'
                        : state === 'selected'
                        ? 'seat-selected'
                        : state === 'unavailable'
                        ? 'bg-gray-50 text-gray-300 cursor-not-allowed border border-gray-100'
                        : 'seat-available'
                    }`}
                    title={label}
                  >
                    {isUnavailable ? '' : label}
                  </button>
                  {/* Aisle gap */}
                  {colIdx + 1 === aisle_after_column && colIdx + 1 < seats_per_row && (
                    <div className="w-4" />
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 mt-4 text-xs text-gray-500">
        <div className="flex items-center gap-1.5">
          <div className="w-5 h-5 rounded seat-available border" />
          <span>{t('seat.available')}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-5 h-5 rounded seat-selected" />
          <span>{t('seat.selected')}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-5 h-5 rounded seat-taken" />
          <span>{t('seat.taken')}</span>
        </div>
      </div>
    </div>
  );
}
