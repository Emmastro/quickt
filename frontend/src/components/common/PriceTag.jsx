import { formatXOF } from '../../utils/format';

export default function PriceTag({ amount, className = '' }) {
  return (
    <span className={`font-bold text-primary-700 ${className}`}>
      {formatXOF(amount)}
    </span>
  );
}
