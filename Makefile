.PHONY: run migrate seed test lint fmt groups shell compose-up compose-down frontend frontend-build frontend-test

run:
	python manage.py runserver

frontend:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

frontend-test:
	cd frontend && npm test -- --run

migrate:
	python manage.py migrate

groups:
	python manage.py create_default_groups

seed:
	@echo "Use /input_handle/ or: python manage.py shell -c 'from Dataset.add_data import ingest_all_tiers; ingest_all_tiers(\"tourist\")'"

shell:
	python manage.py shell

test:
	pytest --cov

lint:
	ruff check .
	bandit -r Dataset Recommender ProblemBuddy -q
	cd frontend && npm run lint

fmt:
	ruff check . --fix

compose-up:
	docker compose up --build

compose-down:
	docker compose down -v
