# QuickT — Product Roadmap

_Last updated: 2026-05-11_

## Vision

Be the default way Togolese travellers discover, book, and pay for intercity bus travel — and the operational backbone that bus agencies in Togo and Francophone West Africa rely on to sell every seat.

## Strategic pillars

1. **Demand-side trust.** A traveller should believe a QuickT-confirmed seat is more reliable than showing up at the gare.
2. **Supply-side leverage.** An agency should sell more seats, lose less to no-shows, and run fewer half-empty buses because they're on QuickT.
3. **Payments-first.** Mobile-money is the rail; we have to be excellent at it (sub-30s confirmations, idempotent refunds, fraud-resistant).
4. **Operate offline-friendly.** Drivers, station agents, and rural customers should not need a constant 4G signal to use us.
5. **Compounding data.** Every booking, refund, no-show, and incident teaches the platform — pricing, capacity, fraud, support routing.

---

## Current state (v0.x — May 2026)

**Customer**
- Email/phone signup with auto-login on register
- Route search by origin/destination/date
- Departure detail + seat selection + booking flow
- Mobile-money payment via Paygate/CinetPay (sandbox in dev; Flooz + T-Money in prod path)
- QR-coded digital tickets in `MyTicketsPage`
- Trip Planner page (reminder for planned trips)
- In-app notifications

**Agency staff**
- Bus fleet management (`ManageBusesPage`)
- Recurring schedules with days-of-week picker (`ManageSchedulesPage`)
- Generate dated departures from a schedule on demand
- Departure list + passenger manifest per departure

**Admin**
- Agency approval queue, route catalog management

**Platform**
- FastAPI + async SQLAlchemy + PostgreSQL on `quickt.emmamurairi.me`
- Ansible-driven deploy, Let's Encrypt TLS, single-VM Docker Compose
- Seed fixtures: 4 agencies, 5 users, 10 routes, 4 buses, 7 schedules, 30-day departure window auto-generated
- AWS SES e-mail, QR generation, JWT auth

**Known gaps used as Phase 1 anchors:** no automated departure regeneration job, no refunds/cancellations flow, no operator settlements, no rating/reviews, no SMS, no offline check-in tooling.

---

## Phase 1 — Make the core loop bulletproof (Q3 2026)

Goal: get one Lomé-based pilot agency to do **100% of their daily seat inventory through QuickT** and have customers actually prefer QuickT to walking to the bus station.

### Customer

- **SMS + WhatsApp ticket delivery.** Email is unreliable in Togo; SMS is the lingua franca. Send booking confirmation, QR-payload-as-text-code fallback, and pre-departure reminders. WhatsApp Business API once volume justifies cost.
- **Cancellation + refund flow.** Customer-initiated cancellation up to a configurable cutoff per agency (e.g. 2h before departure); automatic refund back to the originating mobile-money wallet via Paygate/CinetPay reverse-payment APIs. Partial refunds for late cancellations.
- **Seat-hold + payment timeout.** When a customer picks a seat, hold it for N minutes; release on payment failure. Today seat allocation only happens on confirmed payment; under contention this creates double-bookings.
- **Multi-passenger booking.** One booking, multiple passengers, each with their own ticket QR and full name (required for ID checks at boarding).
- **Saved trips → one-tap rebook.** "Repeat last trip" on the home tab.

### Agency

- **Auto-generate departures cron.** Today an agency clicks "Generate departures" per schedule. Replace with a nightly job that materialises a 14- or 21-day rolling window per active schedule. Surface it in the dashboard as a single "publish horizon" setting.
- **Dynamic pricing per departure.** Override schedule price on individual dates (holidays, last-bus-of-the-day, low-demand corrections).
- **Bus swap / cancellation tool.** Reassign a departure to a different bus (e.g. breakdown), or cancel a departure with automatic refund to all booked passengers and a templated SMS.
- **Boarding check-in app** (PWA, mobile-first). Scan QR → mark `used`. Works offline with later sync. Drives the on-the-ground "this thing is real" moment.
- **Daily settlement statement.** PDF + CSV of all booked seats, paid amounts, refunds, platform commission, net payable. Email-delivered each morning.

### Admin / platform

- **KYC for agencies.** Upload of registration documents (RCCM), national ID of legal representative, bank/MM account verification before payouts can flow.
- **Operational dashboards.** Bookings, refund rate, payment-failure rate, no-show rate, per-route fill rate.
- **Sentry/GlitchTip integration** (already deployed elsewhere on the host) wired through QuickT backend + frontend.

### Reliability/security

- **Idempotency keys on payment callbacks.** Paygate/CinetPay can replay; we must not double-credit.
- **Rate limiting on auth + booking** at nginx + app layer.
- **Backup automation** (PG dumps to S3-compatible storage, daily, 30-day retention).

**Phase 1 exit criteria:** 1 pilot agency doing ≥80% of its Lomé–Kpalimé and Lomé–Atakpamé seat inventory through QuickT, NPS ≥ 40, payment success rate ≥ 95%, refund SLA <24h.

---

## Phase 2 — Liquidity & multi-agency network (Q4 2026 – Q1 2027)

Goal: 8–12 agencies live, cross-agency comparison becomes the customer's reason to use QuickT.

### Customer

- **Agency reviews + ratings.** 1–5 stars on ride completion. Surface average rating + on-time % on search results.
- **Filter / sort** search results by price, departure time, duration, rating, amenities (AC, wifi, USB, reclining seats).
- **Loyalty wallet.** Cashback in QuickT credit on every paid booking; usable on the next booking. Cheaper than direct discounts and increases re-booking rate.
- **Referral program.** Refer a friend → both get FCFA 500 credit on the referee's first paid trip.
- **Push notifications.** Native PWA push for "your bus boards in 1h", "your driver/bus number is XYZ", "your departure is delayed by 30 min".
- **In-app support chat.** Tickets-in-app routed to a per-agency inbox; platform-level escalation for refund disputes.

### Agency

- **Bus seat layout editor.** Today seat layouts are stored as JSONB defaults; expose a visual editor (rows, aisle, unavailable seats, premium seats).
- **Premium / multi-class pricing.** Same departure, different seat tiers (front cabin vs back, sleeper vs standard).
- **Recurring discounts.** "10% off all Mon–Thu morning departures during August" — agency-configurable promo codes and date-range discounts.
- **Customer block-list.** Block customers for documented no-shows or fraud after N strikes.
- **Inventory holds for resellers.** Block X seats on a departure for offline / partner sales.

### Platform

- **Self-serve agency onboarding** with vault-style document upload, automated bank/MM verification, time-to-live before first booking ≤24h.
- **Public agency profile pages** (`/agency/<slug>`) — SEO landing pages with all that agency's routes and schedule.
- **Sitemap + structured data** (`Trip` + `Reservation` schema.org) for Google to index routes and pull QuickT into "Lomé to Kara bus" queries.

### Data / analytics

- **Per-route demand heatmap.** Searches that returned 0 results, by route × day-of-week → product input for sales team to push that agency to add a schedule.
- **Funnel analytics** (search → seat → payment-initiated → paid) via privacy-respecting first-party tracking; PostHog or self-hosted.

---

## Phase 3 — Operational scale and partnerships (Q2 – Q3 2027)

Goal: regional coverage (all major Togo corridors), brand recognition strong enough to negotiate from a position of strength.

### Customer

- **Native Android app** (Capacitor or Flutter wrapping the existing React PWA; the `futurisapp` repo already proves Android delivery on this stack). Offline-first ticket view, push notifications.
- **Multi-leg journeys.** Lomé → Kara → Dapaong as one booking across two operators with a connection guarantee.
- **Group bookings / events.** ≥10 seats with a single payer (schools, churches, NGOs); discounted rate; CSV passenger upload.
- **Travel insurance** (cancellation + accident) per-ticket, distributed in partnership with a local insurer; a few hundred francs per ticket, take-rate platform revenue.
- **French + Ewe + Mina** UI. Today default is French; add the two largest Togolese local languages for southern markets.

### Agency

- **Driver app.** Driver pulls up departure manifest on phone, checks in passengers, marks the bus as `departed`. Powers real-time departure status visible to waiting customers.
- **Real-time GPS tracking.** Driver phone or installed device; surface "your bus is 20 min away from the gare" on the customer ticket. (Bigger lift but a wedge against `mTick` which doesn't offer this.)
- **Yield management hints.** "Your Lomé–Kara Friday departure is 80% sold 48h out — consider adding a second bus." Decision support, not auto-pricing.

### Payments / fintech

- **Stored wallets.** Customers can top-up a QuickT wallet via MM once and pay with one tap, reducing payment-failure churn.
- **Direct integrations** with T-Money (Yas/Togocom) and Flooz (Moov Africa) bypassing aggregators for the largest agencies — better economics on high-volume corridors.
- **Card payments via Stripe-equivalent** (HUB2, FedaPay) for the diaspora and corporate clients.

### Cross-border

- **Benin and Burkina Faso corridor launch.** Lomé–Cotonou is the highest-traffic single corridor in the region; Lomé–Ouagadougou is the strategic northern route. Mirror the Togo playbook with a local sales rep in each market.

---

## Phase 4 — Platform plays (2028)

Treat each of these as a real bet — pursue at most two in parallel based on Phase 3 results.

- **B2B charter / private hire.** Agencies list their idle-time fleet; companies, schools, weddings book them. Take-rate marketplace, higher AOV than ticket sales.
- **Parcel / small-cargo on passenger buses.** Already an informal practice across West Africa; formalise it with QR-tracked parcels riding spare luggage capacity. Counterintuitively often higher margin than seats.
- **Insurance distribution.** Beyond travel insurance: term life, motorbike, health micro-policies sold to the captive monthly-booking customer base.
- **Lender to operators.** Bus financing partnership (à la Gozem's vehicle financing) — refinance an old bus into a newer one against future QuickT GMV. Requires capital partner; high-leverage moat.
- **Open API + white-label.** Power Gozem-style super apps' "transport" tab; power hotel/tour operators bundling buses with stays.

---

## Cross-cutting tracks (continuous)

| Track | Examples |
|-------|----------|
| **Security** | Pen-test before Phase 2; bug bounty when DAU > 5K; PCI-DSS scoping if cards launch; secrets rotation cadence |
| **Reliability** | Multi-AZ Postgres replica before 10K daily bookings; documented runbooks for payment-provider outages |
| **Observability** | Sentry/GlitchTip for FE + BE; structured logs to Grafana Loki; SLOs (p95 search latency, payment confirmation latency) |
| **Compliance** | BCEAO mobile-money escheatment, Togolese PDP (personal-data) law, accessibility (WCAG AA on customer surfaces) |
| **Localization** | French → Ewe + Mina (Phase 3) → Kabye + cross-border tongues |
| **Support quality** | First-response SLA 1h business / 12h overnight, refund SLA 24h; "support" domain already scaffolded |

---

## Anti-roadmap (things we are not building)

These keep coming up; the answer for now is no.

- **Hailing / ride-share.** Gozem owns this; competing head-on burns capital we don't have.
- **Owning fleet.** Asset-heavy, kills our margins, and starts a fight with our suppliers.
- **Crypto rails.** Mobile money already wins on adoption and UX; no Togolese passenger asks for it.
- **Generic e-commerce / events ticketing.** Stay focused on bus until the bus market is saturated.

---

## How to use this roadmap

- **One feature at a time, one phase at a time.** Don't ship the Phase-3 wishlist while Phase-1 refund flow is still broken.
- **Each feature should have a single owner and a measurable success criterion.** "Auto-generate departures cron" succeeds when no agency has manually clicked the generate button for 14 days.
- **Re-plan quarterly.** The market moves; Gozem launched mobile money in 2024 and could enter ticketing tomorrow. Treat this as a living document.

