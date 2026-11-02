.PHONY: up down generate load reconcile test clean

up:
	docker compose up -d
	@echo "Waiting for Postgres to be ready..."
	@sleep 5

down:
	docker compose down -v

generate:
	python src/data_generator.py

load:
	python src/load_to_postgres.py

reconcile:
	python src/sql_reconciler.py

test:
	pytest tests/ -v

clean:
	rm -rf data/raw/* data/processed/* reports/*

run: up generate load reconcile
	@echo "Pipeline finished. Check reports/ or run SQL queries."
