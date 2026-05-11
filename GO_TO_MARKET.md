# QuickT — Go-to-Market Strategy

_Last updated: 2026-05-11_

## 1. Market context

QuickT enters a market that is small in absolute terms but unusually well-prepared for a mobile-first ticketing play:

| Indicator | Value | Source |
|-----------|-------|--------|
| Population | ~8.7M | DataReportal Digital 2025 Togo |
| Urban share | 45.3% | DataReportal Digital 2025 Togo |
| Lomé share of national GDP | ~72% | DataReportal Digital 2025 Togo |
| Mobile subscriptions | 8.7M (>100% penetration; ~SIM count, not unique users) | Africa Business Insight, Sept 2025 |
| Mobile internet users | 3.56M (37% online penetration) | DataReportal Digital 2025 Togo |
| Mobile money users | 3.55M (45.4% penetration) | Togo First, Q1 2024 |
| MM market share | T-Money 60% / Flooz 40% | Togo First, Q1 2024 |
| MM transaction value | CFA ~917B annual; +33% YoY | Togo First, 2025 |
| Road fatalities 2022–24 | 1,826 (avg 608/yr); ~21,000 accidents | Togo First, Nov 2025 |

### What these numbers actually mean

- **3.5M mobile-money users is our serviceable population, not 8.7M.** Anyone outside that pool will buy at the gare; we cannot reach them with our current rail.
- **Lomé is the wedge.** 65% of the population and 72% of GDP sit in one city. Win Lomé and the corridors radiating out of it (Kpalimé, Atakpamé, Sokodé, Kara, Aného, Tsévié) and you have most of the addressable market.
- **The 33% YoY MM transaction-value growth** means each year of delay is real foregone GMV: customers are getting more comfortable paying digitally for higher-value items, and bus tickets (FCFA 1.5K–8K) sit squarely in the comfortable range.
- **Safety is a real lever.** Road fatalities trended down but 600+ deaths/year on Togolese roads keeps "is this bus reliable?" a top question. A verified-agency, verified-bus, verified-driver platform is a credibility play, not just a convenience play.

---

## 2. Customer segments

### a. Urban regular traveller (primary)

- **Profile:** 22–45, Lomé-based, smartphone, employed or trader, takes 1–4 trips/month (visiting family up-country, regional business, weekend escapes).
- **Job-to-be-done:** "Reserve a confirmed seat from my phone tonight so I don't have to leave home at 4am and queue at Akodessewa or Adidogome stations on the off-chance a good bus has space."
- **Pain points today:** Stations are far and chaotic; bus times are word-of-mouth; the "good" agency may already be full; no proof-of-purchase until they hand you a paper stub.
- **Acquisition channel:** Facebook + WhatsApp ads in French, Gozem-driver word-of-mouth, station-adjacent QR-code posters.
- **LTV driver:** Frequency. A traveller who books twice in 30 days is 5× more likely to be a yearly retained user (industry benchmark across BuuPass-style platforms).

### b. Diaspora payer (high-value)

- **Profile:** Togolese in France, Côte d'Ivoire, Ghana, US — pays for parents/relatives' tickets back home.
- **JTBD:** "Send my mother to my sister's wedding in Kara without sending cash by wire, and know that her seat is real."
- **Pain points:** Cross-border money is expensive; family-network bookings rely on someone in Lomé physically going to the station.
- **Acquisition channel:** Diaspora WhatsApp groups, Facebook ads geo-targeted to French/UK/US Togolese communities, partnerships with money-transfer apps (Wave, Wise) for landing-page placement.
- **Why valuable:** They pay in cards/EUR; conversion of a single diaspora payer covers ~3 in-country customer CAC.

### c. Corporate / NGO / institutional (vertical wedge)

- **Profile:** SMEs sending staff between Lomé and regional offices; NGOs running training events; schools moving students; church groups; SOTRAL (the urban network) as a long-term partner.
- **JTBD:** "Buy 25 seats on Wednesday in one transaction with a receipt I can file."
- **Pain points:** Per-person mobile-money is operationally painful; current invoicing options are non-existent.
- **Why important early:** A single corporate account = high-volume, predictable, sticky GMV. Two enterprise wins covers a full month of agency-side ops cost.

### d. Agencies (supply side — co-segment)

We have customers on both sides of the marketplace. Treat agencies as a segment with their own GTM:

- **Tier-1: organised operators** (CTT Rakieta, Etrab, others with multiple buses, fixed schedules). Want to fill empty seats and reduce cash handling.
- **Tier-2: smaller route operators.** Want technology that doesn't require IT staff — sign-up to first-sale ≤24h.
- **Tier-3: informal "tablier" minibuses.** Long-tail. Not Phase-1; consider Phase-3 once we've earned trust.

---

## 3. Competitive landscape

| Competitor | What they do | Strength | Weakness | Our position |
|-----------|--------------|----------|----------|-------------|
| **mTick** | Online + Android ticketing across Burkina, Togo, Benin, Niger, SL. 9 carriers, ~60 cities since 2016. Mobile-money + SMS tickets. | Geographic reach; first-mover; carrier relationships. | Aging UX, no apparent customer growth investment, no agency self-serve, no reviews/ratings/reminders. | Treat them as the incumbent to displace. Faster UX, modern PWA, agency self-serve, customer trust loop (reviews + on-time stats). |
| **Gozem** | Super app: ride-hailing, delivery, "digital ticketing", mobile money (launched late 2024). $30M Series B Feb 2025. 1M+ users. | Distribution; brand; capital; mobile-money product. | Bus ticketing is a small bullet point in a long super-app menu; supply-side relationships with agencies are not their day job. | Risk: they enter aggressively. Mitigation: get exclusive partnerships with the top 5 agencies before they do; offer to be their bus-ticketing back-end (B2B2C play). |
| **Offline gares / agency counters** | Direct sales, cash + MM at the counter. | 100% market share by volume; existing trust. | Painful UX; capacity-blind; no advance assurance for travellers. | This is the real competitor: indifference + habit. We win by being measurably less painful. |
| **Pan-African players (BuuPass, etc.)** | $100M+ GMV; East Africa first, expanding into Ghana/Nigeria. | Capital, tech, regional ambition. | Not focused on Francophone West Africa today; Togo is too small to be priority-one for them. | Watch closely. If they enter, partner or be acquired; don't fight a capital battle. |

### Defensibility playbook

1. **Supply lock.** Exclusivity clauses with top-tier agencies for inventory not sold via station counters (e.g. 100% of online inventory through QuickT for X months in exchange for waived commission).
2. **Customer data flywheel.** Every booking trains demand forecasting, no-show prediction, optimal departure-time recommendations we sell back to agencies.
3. **Mobile-money execution quality.** Sub-30s payment confirmation, idempotent refunds, no double-charges. This is unsexy and very hard; mTick's gaps here are real.
4. **Trust artefacts.** Verified agency badges, on-time stats per departure, reviews → travellers refuse to buy from non-QuickT-verified operators after 12 months.

---

## 4. Positioning & UVP

**Positioning statement:**
> For Togolese travellers who value their time and want to know their seat is real, QuickT is the bus-ticketing platform that confirms your seat in seconds via Flooz or T-Money, delivers a QR ticket to your phone, and only works with verified agencies — unlike walking to the gare, which is unreliable, or mTick, which feels stuck in 2016.

**Customer-facing UVP (French-first market copy):**
- _"Votre place confirmée en 30 secondes."_ (seat confirmed in 30 seconds)
- _"Payez avec Flooz ou T-Money."_
- _"Voyagez avec les agences vérifiées."_

**Agency-facing UVP:**
- _"Vendez la dernière place avant le départ."_ (sell the last seat before departure)
- _"Plus de cash, plus de no-show, plus de comptabilité au stylo."_

---

## 5. The four P's

### Product

Already documented in `ROADMAP.md`. GTM-relevant features that **must ship before broad-market launch**:

- Refund/cancellation flow (single biggest objection in user interviews to anything that isn't cash-at-the-gare)
- SMS ticket delivery (the QR is nice; SMS is non-negotiable)
- 24/7 in-app support inbox (even if hours are limited at first, the channel must exist)
- Multi-passenger booking (a family of four cannot use a product that requires four signups)

### Pricing

- **Customer-facing: free to use.** No booking fee, no service fee. Visible price = price they pay.
- **Agency commission: 5–8% of ticket price.** Benchmarks: BuuPass ~6%, regional bus-ticketing 4–10% depending on volume. Start higher (8%) to fund ops; introduce a volume sliding scale (5% above N bookings/month) as agencies grow on the platform.
- **Payment-rail pass-through.** Mobile-money fees from CinetPay/Paygate (~1.5–2.5% depending on operator) are netted out of the agency settlement, not added to customer price.
- **Phase-2 surcharges:** premium-seat fees, late cancellation fees, optional travel insurance (~FCFA 200/ticket with insurer split).

### Promotion (marketing playbook)

**Pre-launch (4–6 weeks before each city launch):**

- Partner with 1 anchor agency per city, exclusive-launch deal.
- Influencer seeding: 3–5 mid-tier Togolese travel/lifestyle creators on TikTok + Instagram (cost: travel + FCFA 50K–200K each).
- French-language press: Togo First, Republic of Togo, l'Économiste du Togo — pitch the "tech-against-bus-station-chaos" angle.

**Launch week:**

- Geo-fenced Facebook + Instagram ads, audience: 22–45 in Lomé + targeted city, interest in "Travel" + "Mobile money".
- Promo code: first booking 25% off (capped at FCFA 2,000), expires in 30 days. Cap budget; this is acquisition, not subsidy.
- Bus-station QR-poster blitz, partnered with anchor agency.

**Always-on:**

- Referral: refer-a-friend, both get FCFA 500 on the referee's first paid trip. Cap at FCFA 1,500 lifetime per referrer.
- Retargeting Facebook / Google ads to anyone who searched but didn't book (high-intent, cheap clicks).
- Newsletter to bookers: monthly "new routes / promo / upcoming features".
- SEO: indexed agency + route pages (Phase 2). "[city] [city] bus" is a real query; capture it.

**Earned media plays:**

- Annual "État de la mobilité au Togo" report from QuickT data — newsroom catnip, repeat content for 2–3 years.
- Heatmap of busiest routes / busiest weekends — local news loves a chart.

### Place (channels & distribution)

- **Web app PWA**, mobile-first; default channel.
- **Direct WhatsApp booking** (Phase 1.5): user texts a QuickT business number, gets a magic link. Captures the WhatsApp-first majority that won't install an app.
- **USSD fallback** (Phase 2): partnership with Yas/Moov to expose a short-code menu for non-smartphone users. Critical for tier-2 cities and elderly customers.
- **Embedded checkout in partner apps:** Phase 3 super-app partnership: power the bus-ticketing tab inside another app (Gozem's competitor, a money-transfer app, a hotel booking app).
- **Physical agent network:** Phase 2 — a small commission to mobile-money agents who help non-digital customers book. Pays a token (FCFA 100–200) per assisted booking.

---

## 6. Supply-side: agency onboarding

QuickT is a chicken-and-egg marketplace. The first 90 days are about supply, not demand.

### Target list — Phase 1 (Lomé and surroundings)

Anchor candidates, in order of strategic value:

1. **CTT Rakieta** — fleet size, all-Togo coverage. Hardest to land; biggest unlock.
2. **STIF Transport** (already in seed data; placeholder until confirmed) — Lomé-based; medium fleet.
3. **Etrab** — established southern routes.
4. Three or four mid-sized regional operators on the Lomé–Kara corridor.

### Pitch to agencies

The deck is one A4 page:

- **"We bring you the digital customer you're losing today."** Most Lomé under-30s do not show up at your counter; they call a relative or skip the trip.
- **"You keep 92–95% of the ticket price."** Show the math against their current operational cost (cash handling, station rent, no-shows).
- **"Setup is free. No software to install. No IT team."** A QuickT rep does the first onboarding in person, in 60 minutes.
- **"You get paid every 24h via mobile money."** Critical: Togolese operators are sensitive to cash-flow timing; weekly or monthly payouts are a deal-breaker.
- **"Exclusive launch deal: 0% commission for your first 90 days."** Cheap incentive against a real pain.

### Onboarding playbook

| Step | Owner | Time |
|------|-------|------|
| Sales meeting at agency office | QuickT sales | 1 day |
| KYC docs collected (RCCM, ID, MM account) | QuickT ops | 24h |
| Onboarding visit: enter buses, routes, schedules into dashboard with agency staff | QuickT field rep | half-day |
| First test booking by QuickT rep + agency staff | both | 1h |
| First real booking | customer | depends on demand |
| 30-day check-in: review settlement statements, fix friction | QuickT account manager | 1h |

KPI: time-to-first-real-booking from KYC ≤ 7 days.

### Agency retention

- Weekly automated WhatsApp summary: bookings, payouts, top routes, "you had 3 sold-out departures last week — consider adding a 2nd bus on these days".
- Quarterly in-person review with top-10 agencies.
- Tiered support SLA: Tier-1 agencies get a dedicated WhatsApp line; tier-2 get the shared support inbox.

---

## 7. Launch sequencing

| Phase | Cities/corridors | Timeline | Target agencies live | Monthly GMV target |
|-------|------------------|----------|---------------------|---------------------|
| Pilot | Lomé ↔ Kpalimé, Lomé ↔ Atakpamé | Q3 2026 | 1 anchor | FCFA 5M |
| Beachhead | + Lomé ↔ Sokodé, Lomé ↔ Kara, Lomé ↔ Aného | Q4 2026 | 4–6 | FCFA 30M |
| National | All major Togo corridors incl. Kara ↔ Dapaong | Q1–Q2 2027 | 10–15 | FCFA 100M |
| Cross-border | + Lomé ↔ Cotonou, Lomé ↔ Accra, Lomé ↔ Ouagadougou | Q3–Q4 2027 | 18–25 | FCFA 300M |
| Regional | + secondary cross-border (Benin–Burkina–Niger) | 2028 | 40+ | FCFA 800M+ |

**Why this sequence:**
- The Lomé ↔ Kpalimé corridor has the highest single-corridor density (short distance, multiple daily departures, weekend leisure traffic). It's where unit-economic learning is fastest.
- Lomé ↔ Cotonou is the highest single cross-border ticket volume in West Africa; opens currency / VAT complexity, so deferred until Togo operations are dialed.
- Cross-border into Burkina is a strategic move against mTick's home turf — only worth doing once we're operationally stronger than them in Togo.

---

## 8. Funding & resource shape (illustrative)

Order-of-magnitude only; real numbers depend on traction.

| Phase | Headcount | Burn / month | Notes |
|-------|-----------|--------------|-------|
| Pilot | 3 (founder/eng, 1 sales/ops, 1 support) | FCFA 4–6M | Customer-funded if pilot agency commits a minimum revenue |
| Beachhead | 6 (+1 backend, +1 designer/PM, +1 sales) | FCFA 12–15M | Seed funding ($300–500K) or revenue-based |
| National | 12 (+ ops manager, + finance, + 2 agency-success reps) | FCFA 25–35M | Pre-Series-A; need to demonstrate unit economics |
| Cross-border | 25+ | FCFA 60M+ | Series A; track Gozem's playbook for francophone scale |

Comparables: Gozem $30M Series B for a multi-vertical super app across 4 countries; BuuPass smaller rounds but $100M+ GMV at scale. A focused Togo-then-region bus play should be capital-light by comparison until cross-border.

---

## 9. KPIs (the only ones that matter)

**Customer**
- Monthly active bookers
- First-booking → second-booking rate within 30 days (target: ≥35%)
- Payment success rate (target: ≥95%)
- NPS (target: ≥40 at end of Phase 1)
- Refund-fulfilment time (target: <24h)

**Agency**
- Number of agencies live
- Agency MoM revenue retention
- Inventory share: % of an agency's seats sold via QuickT vs counter
- Time-to-first-booking from KYC

**Marketplace**
- GMV
- Take rate (commission / GMV)
- Search → paid conversion
- 0-result search rate per corridor (demand signal for supply team)
- Net contribution per booking (revenue − payment fees − support cost − refund losses)

---

## 10. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Gozem enters bus ticketing aggressively | Medium | High | Lock exclusivity with top 5 agencies in Phase 1; explore being their back-end |
| Mobile-money outage at Flooz or T-Money during peak | High | Medium | Multi-provider integration (Paygate + CinetPay + direct), graceful degradation, transparent comms |
| Payment fraud / chargebacks | Medium | Medium | Velocity rules per phone number + device; manual review queue; ID match for high-value diaspora payments |
| One agency dominates supply → bargaining-power flip | Medium | High | Diversify; never let any single agency exceed 35% of platform GMV |
| Regulatory: BCEAO mobile-money rules tighten | Low | Medium | Stay within agent of an EMI; do not become a payment provider ourselves; lawyer on retainer |
| Talent: hiring engineering in Togo is hard | High | Medium | Remote Francophone-Africa hiring (Côte d'Ivoire, Senegal, Cameroon); contractors via Andela-style platforms |
| Currency: CFA vs EUR for cross-border payouts | Low (Phase 1–2) | Medium (Phase 3) | Operate WAEMU-internal in Phase 1–3; defer non-CFA expansion |
| Safety incident on a partner-agency bus | Medium | High | Verified-agency criteria including roadworthiness checks; immediate suspension protocol; comms playbook |

---

## 11. First 100 days, concretely

Week 1–2
- Confirm pilot agency LOI (letter of intent), KYC docs.
- Ship: refund flow, multi-passenger booking, SMS confirmations, auto-departure-generation cron.

Week 3–4
- In-person agency onboarding visit; train 2–3 of their counter staff to use the dashboard.
- Soft-launch to friends-and-family (50 bookings target).

Week 5–8
- Public launch in Lomé corridor (Lomé–Kpalimé, Lomé–Atakpamé).
- Facebook + Instagram ads at FCFA 200K/month budget.
- Press: 1–2 Togolese tech/business outlets.
- Daily standup with anchor agency; weekly product iteration on whatever friction is highest.

Week 9–12
- Add 2 more agencies on the same corridors → first time customers can compare options on QuickT.
- Ship: ratings/reviews, premium seats, dynamic pricing per departure.
- Begin onboarding 3rd–6th agency.

Week 13–14 (Day 90)
- 200 monthly active bookers, ≥35% 30-day repeat rate, payment success >95%, ≥4 agencies live, NPS measured. Hit these or re-plan; do not push to the beachhead phase until they hold for 30 days.

---

## Sources

- [DataReportal — Digital 2025: Togo](https://datareportal.com/reports/digital-2025-togo)
- [Africa Business Insight — Togo's mobile penetration exceeds 100% (Sept 2025)](https://africabusinessinsight.com/togos-mobile-penetration-exceeds-100-for-first-time-as-subscriptions-reach-8-7-million/)
- [Togo First — Mobile money penetration and operator market share](https://www.togofirst.com/en/telecom/2810-15076-togocom-launches-new-subsidiary-to-manage-mobile-money-segment)
- [Togo First — Road deaths fell between 2022 and 2024](https://www.togofirst.com/en/transport/2811-17678-togo-road-deaths-fell-between-2022-and-2024-data-show)
- [Petit Futé — Transport in Togo (operators)](https://www.petitfute.co.uk/p107-togo/se-deplacer/)
- [mTick — Fabrique des Mobilités](https://wiki.lafabriquedesmobilites.fr/wiki/Mtick)
- [TechCrunch — Gozem $30M Series B](https://techcrunch.com/2025/02/26/gozem-nets-30m-to-expand-vehicle-financing-digital-banking-in-francophone-africa/)
- [TechCabal — Gozem expands into mobile money](https://techcabal.com/2025/10/14/togos-gozem-expands-into-mobile-money-with-new-fintech-platform/)
- [Techpoint Africa — BuuPass acquires QuickBus](https://techpoint.africa/news/kenyan-buupass-acquires-quickbus/)
- [Stanford GSB — Disrupting African Travel (BuuPass)](https://www.gsb.stanford.edu/insights/short-takes-disrupting-african-travel-one-ticket-time)
- [CinetPay — Products & pricing](https://cinetpay.com/products/payments)
- [Wise — Payment methods in Togo](https://wise.com/gb/hub/payment-methods/togo)
