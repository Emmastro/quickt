-- QuickT: Initial schema — users, agencies, routes

-- Enums
DO $$ BEGIN
    CREATE TYPE user_role_enum AS ENUM ('customer', 'agency_staff', 'admin');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE agency_status_enum AS ENUM ('pending', 'approved', 'suspended');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Agencies (created first because users reference it)
CREATE TABLE IF NOT EXISTS agencies (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL UNIQUE,
    slug            VARCHAR(255) NOT NULL UNIQUE,
    description     TEXT,
    logo_url        VARCHAR(500),
    phone           VARCHAR(20) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    address         VARCHAR(500) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    region          VARCHAR(100) NOT NULL,
    status          agency_status_enum NOT NULL DEFAULT 'pending',
    rating          NUMERIC(3,2) NOT NULL DEFAULT 0.00,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    approved_at     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_agencies_slug ON agencies (slug);
CREATE INDEX IF NOT EXISTS idx_agencies_region ON agencies (region);
CREATE INDEX IF NOT EXISTS idx_agencies_status ON agencies (status);

-- Users
CREATE TABLE IF NOT EXISTS users (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email               VARCHAR(255) NOT NULL UNIQUE,
    phone               VARCHAR(20) NOT NULL,
    full_name           VARCHAR(255) NOT NULL,
    hashed_password     VARCHAR(255) NOT NULL,
    role                user_role_enum NOT NULL DEFAULT 'customer',
    city                VARCHAR(100),
    preferred_language  VARCHAR(5) NOT NULL DEFAULT 'fr',
    agency_id           INTEGER REFERENCES agencies(id),
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_phone ON users (phone);
CREATE INDEX IF NOT EXISTS idx_users_agency_id ON users (agency_id);

-- Routes
CREATE TABLE IF NOT EXISTS routes (
    id                          SERIAL PRIMARY KEY,
    origin_city                 VARCHAR(100) NOT NULL,
    destination_city            VARCHAR(100) NOT NULL,
    distance_km                 INTEGER,
    estimated_duration_minutes  INTEGER NOT NULL,
    is_active                   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_route_origin_dest UNIQUE (origin_city, destination_city)
);

CREATE INDEX IF NOT EXISTS idx_routes_origin ON routes (origin_city);
CREATE INDEX IF NOT EXISTS idx_routes_destination ON routes (destination_city);
