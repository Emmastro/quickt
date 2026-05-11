/**
 * Format amount in XOF (FCFA).
 * Example: 2500 -> "2 500 FCFA"
 */
export function formatXOF(amount) {
  if (amount == null) return '';
  const num = Number(amount);
  const formatted = new Intl.NumberFormat('fr-FR', {
    maximumFractionDigits: 0,
  }).format(num);
  return `${formatted} FCFA`;
}

/**
 * Format duration in minutes to human-readable.
 * Example: 150 -> "2h 30min"
 */
export function formatDuration(minutes) {
  if (!minutes) return '';
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours && mins) return `${hours}h ${mins}min`;
  if (hours) return `${hours}h`;
  return `${mins}min`;
}

/**
 * Format date string to localized display.
 */
export function formatDate(dateStr, locale = 'fr-FR') {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString(locale, {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format time string (HH:MM or HH:MM:SS) to display.
 */
export function formatTime(timeStr) {
  if (!timeStr) return '';
  return timeStr.substring(0, 5);
}
