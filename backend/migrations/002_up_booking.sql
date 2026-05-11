-- Buses table
CREATE TABLE IF NOT EXISTS buses (
    id SERIAL PRIMARY KEY,
    agency_id INTEGER NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    model VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    seat_layout JSONB NOT NULL DEFAULT '{"rows": 10, "seats_per_row": 4, "aisle_after_column": 2, "unavailable_seats": [], "labels": []}',
    amenities JSONB NOT NULL DEFAULT '[]',
    image_url VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_buses_agency_id ON buses(agency_id);

-- Schedules table
CREATE TABLE IF NOT EXISTS schedules (
    id SERIAL PRIMARY KEY,
    agency_id INTEGER NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
    route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    bus_id INTEGER NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
    departure_time TIME NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    days_of_week JSONB NOT NULL DEFAULT '[0,1,2,3,4,5,6]',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_schedules_agency_id ON schedules(agency_id);
CREATE INDEX IF NOT EXISTS idx_schedules_route_id ON schedules(route_id);
CREATE INDEX IF NOT EXISTS idx_schedules_bus_id ON schedules(bus_id);

-- Departure status enum
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'departure_status_enum') THEN
        CREATE TYPE departure_status_enum AS ENUM ('scheduled', 'boarding', 'departed', 'completed', 'cancelled');
    END IF;
END$$;

-- Departures table
CREATE TABLE IF NOT EXISTS departures (
    id SERIAL PRIMARY KEY,
    schedule_id INTEGER NOT NULL REFERENCES schedules(id) ON DELETE CASCADE,
    agency_id INTEGER NOT NULL REFERENCES agencies(id) ON DELETE CASCADE,
    route_id INTEGER NOT NULL REFERENCES routes(id) ON DELETE CASCADE,
    bus_id INTEGER NOT NULL REFERENCES buses(id) ON DELETE CASCADE,
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    status departure_status_enum NOT NULL DEFAULT 'scheduled',
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL,
    booked_seats JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_departure_schedule_date UNIQUE (schedule_id, departure_date)
);

CREATE INDEX IF NOT EXISTS idx_departures_schedule_id ON departures(schedule_id);
CREATE INDEX IF NOT EXISTS idx_departures_agency_id ON departures(agency_id);
CREATE INDEX IF NOT EXISTS idx_departures_route_id ON departures(route_id);
CREATE INDEX IF NOT EXISTS idx_departures_date ON departures(departure_date);

-- Ticket status enum
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ticket_status_enum') THEN
        CREATE TYPE ticket_status_enum AS ENUM ('reserved', 'confirmed', 'cancelled', 'used', 'expired');
    END IF;
END$$;

-- Tickets table
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    departure_id INTEGER NOT NULL REFERENCES departures(id) ON DELETE CASCADE,
    customer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    seat_number VARCHAR(10) NOT NULL,
    passenger_name VARCHAR(255) NOT NULL,
    passenger_phone VARCHAR(20) NOT NULL,
    status ticket_status_enum NOT NULL DEFAULT 'reserved',
    price NUMERIC(12, 2) NOT NULL,
    qr_code_url VARCHAR(500),
    booking_reference VARCHAR(20) NOT NULL,
    reserved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    confirmed_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    cancellation_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_ticket_departure_seat UNIQUE (departure_id, seat_number)
);

CREATE INDEX IF NOT EXISTS idx_tickets_code ON tickets(code);
CREATE INDEX IF NOT EXISTS idx_tickets_departure_id ON tickets(departure_id);
CREATE INDEX IF NOT EXISTS idx_tickets_customer_id ON tickets(customer_id);
CREATE INDEX IF NOT EXISTS idx_tickets_booking_ref ON tickets(booking_reference);
