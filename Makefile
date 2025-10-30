COMPOSE ?= docker compose

.PHONY: fe be up db-reset

fe:
$(COMPOSE) up frontend

be:
$(COMPOSE) up backend

up:
$(COMPOSE) up frontend backend

db-reset:
mkdir -p backend/instance
rm -f backend/instance/bluesea.db
$(COMPOSE) run --rm backend python -m bluesea_app.seeds
