"""
Raw SQL migration runner for QuickT.

Convention:
    migrations/NNN_up_<name>.sql   -- forward migration
    migrations/NNN_down_<name>.sql -- rollback migration

Tracking table:
    schema_migrations(filename TEXT PRIMARY KEY, applied_at TIMESTAMPTZ)

Usage:
    uv run python scripts/migrate.py up
    uv run python scripts/migrate.py down
    uv run python scripts/migrate.py status
"""
import asyncio
import sys
from pathlib import Path

import asyncpg
from dotenv import load_dotenv
import os

MIGRATIONS_DIR = Path(__file__).parent.parent / "migrations"
TRACKING_TABLE = "schema_migrations"

load_dotenv(Path(__file__).parent.parent / ".env")


def _get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "")
    if not url:
        sys.exit("ERROR: DATABASE_URL is not set.")
    return url.replace("postgresql+asyncpg://", "postgresql://")


async def _bootstrap(conn):
    await conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TRACKING_TABLE} (
            filename   TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)


async def _applied(conn):
    rows = await conn.fetch(f"SELECT filename FROM {TRACKING_TABLE} ORDER BY filename")
    return [r["filename"] for r in rows]


def _up_files():
    return sorted(MIGRATIONS_DIR.glob("*_up_*.sql"))


async def cmd_up(conn):
    await _bootstrap(conn)
    done = set(await _applied(conn))
    pending = [f for f in _up_files() if f.name not in done]
    if not pending:
        print("Nothing to apply -- all migrations are up to date.")
        return
    for path in pending:
        sql = path.read_text()
        print(f"  Applying  {path.name} ...", end=" ", flush=True)
        await conn.execute(sql)
        await conn.execute(
            f"INSERT INTO {TRACKING_TABLE} (filename) VALUES ($1)", path.name
        )
        print("done")
    print(f"\n{len(pending)} migration(s) applied.")


async def cmd_down(conn):
    await _bootstrap(conn)
    done = await _applied(conn)
    if not done:
        print("Nothing to roll back.")
        return
    latest_up = done[-1]
    num = latest_up.split("_")[0]
    down_glob = list(MIGRATIONS_DIR.glob(f"{num}_down_*.sql"))
    if not down_glob:
        sys.exit(f"ERROR: no down migration found for {latest_up}")
    down_path = down_glob[0]
    print(f"  Rolling back  {latest_up} ...", end=" ", flush=True)
    await conn.execute(down_path.read_text())
    await conn.execute(f"DELETE FROM {TRACKING_TABLE} WHERE filename = $1", latest_up)
    print("done")


async def cmd_status(conn):
    await _bootstrap(conn)
    done = set(await _applied(conn))
    for path in _up_files():
        status = "applied" if path.name in done else "pending"
        print(f"{status:<10} {path.name}")


_ADVISORY_LOCK_KEY = 8675310


async def main(command: str):
    url = _get_database_url()
    conn = await asyncpg.connect(url)
    try:
        if command in ("up", "down"):
            await conn.execute(f"SELECT pg_advisory_lock({_ADVISORY_LOCK_KEY})")
            try:
                await (cmd_up if command == "up" else cmd_down)(conn)
            finally:
                await conn.execute(f"SELECT pg_advisory_unlock({_ADVISORY_LOCK_KEY})")
        elif command == "status":
            await cmd_status(conn)
        else:
            sys.exit(f"Unknown command '{command}'. Use: up | down | status")
    finally:
        await conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/migrate.py <up|down|status>")
    asyncio.run(main(sys.argv[1]))
