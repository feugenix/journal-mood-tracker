# Makefile for journal-mood-tracker

.PHONY: lint-be

lint-be:
	docker compose -f docker-compose.test.yml run lint
