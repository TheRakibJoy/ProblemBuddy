.PHONY: run migrate seed test lint fmt groups shell compose-up compose-down

run:
	python manage.py runserver

migrate:
	python manage.py migrate

groups:
	python manage.py create_default_groups

seed:
	@echo "Use the /input_handle/ page or: python manage.py shell -c 'from Dataset.add_data import ingest_all_tiers; ingest_all_tiers(\"tourist\")'"

shell:
	python manage.py shell

test:
	pytest --cov

lint:
	ruff check .
	bandit -r Dataset Recommender ProblemBuddy -q

fmt:
	ruff check . --fix

compose-up:
	docker compose up --build

compose-down:
	docker compose down -v
