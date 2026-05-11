-- Payment enums
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_method_enum') THEN
        CREATE TYPE payment_method_enum AS ENUM ('flooz', 't_money');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_status_enum') THEN
        CREATE TYPE payment_status_enum AS ENUM ('pending', 'confirmed', 'failed', 'refunded');
    END IF;
END$$;

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    booking_reference VARCHAR(20) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    method payment_method_enum NOT NULL,
    phone VARCHAR(20) NOT NULL,
    status payment_status_enum NOT NULL DEFAULT 'pending',
    provider_tx_id VARCHAR(255),
    provider_status VARCHAR(100),
    confirmed_at TIMESTAMPTZ,
    refunded_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_payments_booking_ref ON payments(booking_reference);
