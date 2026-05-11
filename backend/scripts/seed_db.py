#!/usr/bin/env python3
"""
Fixture loader for QuickT. Reads JSON files from data/ and loads them in FK order.
Usage: PYTHONPATH=. uv run python scripts/seed_db.py
"""
import asyncio
import json
import logging
import os
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import hash_password
from app.database import Base, build_engine
from app.domains.auth.models import User
from app.domains.agencies.models import Agency
from app.domains.routes.models import Route
from app.domains.buses.models import Bus
from app.domains.schedules.models import Schedule
from app.domains.departures.models import Departure, DepartureStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReferenceRegistry:
    def __init__(self):
        self._registry: dict[str, dict[str, dict]] = {}

    def register(self, model_name, lookup_field, lookup_value, pk_value):
        self._registry.setdefault(model_name, {}).setdefault(lookup_field, {})[
            lookup_value
        ] = pk_value

    def lookup(self, model_name, lookup_field, lookup_value):
        try:
            return self._registry[model_name][lookup_field][lookup_value]
        except KeyError:
            available = list(
                self._registry.get(model_name, {}).get(lookup_field, {}).keys()
            )
            raise ValueError(
                f"Cannot resolve {model_name}.{lookup_field}={lookup_value!r}. "
                f"Available: {available}"
            )


class FixtureLoader:
    def __init__(self, fixtures_dir, session_factory=None):
        self.fixtures_dir = Path(fixtures_dir)
        self.registry = ReferenceRegistry()
        self.session_factory = session_factory or async_sessionmaker(
            bind=build_engine(os.getenv("DATABASE_URL")),
            class_=AsyncSession,
            expire_on_commit=False,
        )
        self.load_order = [
            ("agencies", Agency),
            ("users", User),
            ("routes", Route),
            ("buses", Bus),
            ("schedules", Schedule),
        ]
        self.reference_fields = {
            "users": {
                "agency_name": ("agencies", "name", "agency_id"),
            },
            "buses": {
                "agency_name": ("agencies", "name", "agency_id"),
            },
            "schedules": {
                "agency_name": ("agencies", "name", "agency_id"),
                "route_ref": ("routes", "_ref", "route_id"),
                "bus_ref": ("buses", "_ref", "bus_id"),
            },
        }

    def load_file(self, filename):
        filepath = self.fixtures_dir / f"{filename}.json"
        if not filepath.exists():
            return []
        with open(filepath) as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]

    def process_record(self, model_class, data):
        processed = data.copy()
        meta = {}
        model_name = model_class.__tablename__

        if "_ref" in processed:
            meta["_ref"] = processed.pop("_ref")

        if model_class == User and "password" in processed:
            processed["hashed_password"] = hash_password(processed.pop("password"))

        for ref_field, (
            lookup_model,
            lookup_key,
            target_field,
        ) in self.reference_fields.get(model_name, {}).items():
            if ref_field in processed:
                if processed[ref_field] is not None:
                    processed[target_field] = self.registry.lookup(
                        lookup_model, lookup_key, processed[ref_field]
                    )
                del processed[ref_field]

        # Parse datetime / time strings
        for field in list(processed.keys()):
            val = processed.get(field)
            if not isinstance(val, str):
                continue
            if "T" in val or val.endswith("Z"):
                try:
                    processed[field] = datetime.fromisoformat(
                        val.replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    pass
            elif len(val) in (5, 8) and val[2] == ":" and val[:2].isdigit():
                try:
                    processed[field] = time.fromisoformat(val)
                except (ValueError, TypeError):
                    pass

        return processed, meta

    def register_instance(self, model_name, instance, meta):
        if hasattr(instance, "id"):
            self.registry.register(model_name, "id", instance.id, instance.id)
        if meta.get("_ref"):
            self.registry.register(model_name, "_ref", meta["_ref"], instance.id)
        if model_name == "users" and hasattr(instance, "email"):
            self.registry.register(model_name, "email", instance.email, instance.id)
        if model_name == "agencies" and hasattr(instance, "name"):
            self.registry.register(model_name, "name", instance.name, instance.id)

    async def load_all(self):
        async with self.session_factory() as session:
            # Truncate
            table_names = [m.__tablename__ for _, m in reversed(self.load_order)]
            existing = await session.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
            existing_set = {r[0] for r in existing}
            to_truncate = [t for t in table_names if t in existing_set]
            if to_truncate:
                await session.execute(
                    text(
                        f"TRUNCATE TABLE {', '.join(to_truncate)} RESTART IDENTITY CASCADE"
                    )
                )
            await session.commit()

            # Load
            for filename, model_class in self.load_order:
                records = self.load_file(filename)
                for record in records:
                    processed, meta = self.process_record(model_class, record)
                    instance = model_class(**processed)
                    session.add(instance)
                    await session.flush()
                    self.register_instance(
                        model_class.__tablename__, instance, meta
                    )
                await session.commit()
                if records:
                    logger.info(f"Loaded {len(records)} {filename}")

            # Generate concrete departures for the next 30 days from each schedule
            sched_result = await session.execute(select(Schedule))
            schedules = list(sched_result.scalars().all())
            bus_result = await session.execute(select(Bus))
            buses_by_id = {b.id: b for b in bus_result.scalars().all()}
            today = date.today()
            total_deps = 0
            for sched in schedules:
                bus = buses_by_id.get(sched.bus_id)
                if not bus:
                    continue
                for offset in range(30):
                    d = today + timedelta(days=offset)
                    if d.weekday() not in sched.days_of_week:
                        continue
                    session.add(
                        Departure(
                            schedule_id=sched.id,
                            agency_id=sched.agency_id,
                            route_id=sched.route_id,
                            bus_id=sched.bus_id,
                            departure_date=d,
                            departure_time=sched.departure_time,
                            price=sched.price,
                            status=DepartureStatus.scheduled,
                            total_seats=bus.capacity,
                            available_seats=bus.capacity,
                            booked_seats=[],
                        )
                    )
                    total_deps += 1
            await session.commit()
            if total_deps:
                logger.info(f"Generated {total_deps} departures (30-day window)")

            # Sync sequences
            seqs = await session.execute(
                text("""
                SELECT c.relname, s.relname FROM pg_class c
                JOIN pg_depend d ON d.refobjid = c.oid
                JOIN pg_class s ON s.oid = d.objid
                WHERE c.relkind = 'r' AND s.relkind = 'S'
            """)
            )
            for table_name, seq_name in seqs:
                try:
                    max_id = (
                        await session.execute(
                            text(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
                        )
                    ).scalar()
                    if max_id and max_id > 0:
                        await session.execute(
                            text(f"SELECT setval('{seq_name}', {max_id})")
                        )
                except Exception:
                    pass
            await session.commit()
            logger.info("Done!")


async def main():
    loader = FixtureLoader(Path(__file__).parent.parent / "data")
    await loader.load_all()


if __name__ == "__main__":
    import sys

    sys.path.append(os.getcwd())
    asyncio.run(main())
