.PHONY: help dev-web dev-api update-web update-api update dev

help:
	@echo "Available commands:"
	@echo "  make dev-web                - Starts the web development server (Next.js)"
	@echo "  make dev-api                - Starts the API development server (FastAPI)"
	@echo "  make update-web             - Updates dependencies for the web"
	@echo "  make update-api             - Updates dependencies for the API"
	@echo "  make update                 - Updates dependencies for both web and API"
	@echo "  make dev                    - Starts both web and API development servers"

dev-web:
	@echo "Starting web development server..."
	@cd web && pnpm run dev

dev-api:
	@echo "Starting API development server..."
	@cd api && uv run fastapi dev ./src/main.py

update-web:
	@echo "Updating dependencies for web..."
	@cd web && pnpm update --latest --recursive

update-api:
	@echo "Updating dependencies for API..."
	@cd api && uv lock --upgrade && uv sync

update:
	@echo "Updating dependencies for both web and API..."
	@make update-web
	@make update-api

dev:
	@echo "Starting both web and API development servers..."
	@trap 'kill -INT $$WEB_PID $$API_PID 2>/dev/null; wait $$WEB_PID $$API_PID 2>/dev/null' INT TERM; \
	make dev-web & WEB_PID=$$!; \
	make dev-api & API_PID=$$!; \
	wait $$WEB_PID $$API_PID; \
	trap - INT TERM
