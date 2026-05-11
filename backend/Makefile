# Backend Makefile for QuickT
DB_HOST      ?= localhost
DB_PORT      ?= 5432
DB_USER      ?= postgres
DB_PASS      ?= postgres
DB_NAME      ?= quickt_db
DB_NAME_TEST ?= quickt_db_test
APP_PORT     ?= 8095

_ASYNC_URL      := postgresql+asyncpg://$(DB_USER):$(DB_PASS)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)
_ASYNC_URL_TEST := postgresql+asyncpg://$(DB_USER):$(DB_PASS)@$(DB_HOST):$(DB_PORT)/$(DB_NAME_TEST)

.PHONY: help install dev test seed setup reset setup-test reset-test \
        db-create db-drop db-test-create db-test-drop \
        migrate-up migrate-down migrate-status migrate-test-up \
        load-fixtures reset-with-fixtures

help:
	@echo ""
	@echo "  Setup"
	@echo "    make setup              install + create DB + migrate"
	@echo "    make reset              drop + create + migrate"
	@echo "    make reset-with-fixtures  reset + seed"
	@echo "    make setup-test         install + create test DB + migrate"
	@echo "    make reset-test         drop test DB + recreate + migrate"
	@echo ""
	@echo "  Development"
	@echo "    make dev                start dev server on :$(APP_PORT)"
	@echo "    make test               run test suite"
	@echo "    make seed               load demo data"
	@echo ""

install:
	uv sync

db-create:
	@docker exec postgres psql -U $(DB_USER) -c "CREATE DATABASE $(DB_NAME);" 2>/dev/null \
	  && echo "Created database '$(DB_NAME)'." \
	  || echo "Database '$(DB_NAME)' may already exist."

db-drop:
	@docker exec postgres psql -U $(DB_USER) -c "DROP DATABASE IF EXISTS $(DB_NAME);" \
	  && echo "Dropped database '$(DB_NAME)'."

db-test-create:
	@docker exec postgres psql -U $(DB_USER) -c "CREATE DATABASE $(DB_NAME_TEST);" 2>/dev/null \
	  && echo "Created test database '$(DB_NAME_TEST)'." \
	  || echo "Test database '$(DB_NAME_TEST)' may already exist."

db-test-drop:
	@docker exec postgres psql -U $(DB_USER) -c "DROP DATABASE IF EXISTS $(DB_NAME_TEST);" \
	  && echo "Dropped test database '$(DB_NAME_TEST)'."

migrate-up:
	DATABASE_URL=$(_ASYNC_URL) uv run python scripts/migrate.py up

migrate-down:
	DATABASE_URL=$(_ASYNC_URL) uv run python scripts/migrate.py down

migrate-status:
	DATABASE_URL=$(_ASYNC_URL) uv run python scripts/migrate.py status

migrate-test-up:
	DATABASE_URL=$(_ASYNC_URL_TEST) uv run python scripts/migrate.py up

seed:
	PYTHONPATH=. DATABASE_URL=$(_ASYNC_URL) uv run python scripts/seed_db.py

load-fixtures: seed

dev:
	DATABASE_URL=$(_ASYNC_URL) uv run uvicorn app.main:app --reload --host 0.0.0.0 --port $(APP_PORT)

test: migrate-test-up
	DATABASE_URL=$(_ASYNC_URL_TEST) uv run pytest tests/ -v

setup: install db-create migrate-up
reset: db-drop db-create migrate-up
setup-test: install db-test-create migrate-test-up
reset-test: db-test-drop db-test-create migrate-test-up
reset-with-fixtures: db-drop db-create migrate-up load-fixtures
