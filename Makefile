GREEN = $$(printf '\033[0;32m')
YELLOW = $$(printf '\033[0;33m')
RED = $$(printf '\033[0;31m')
RESET = $$(printf '\033[0m')

all: build

logs:
	@docker logs mealwise_dev

test-unit:
	@echo "-----| $(GREEN)Starting containers in test mode$(RESET) |-----"
	@docker-compose -f docker-compose.test.yml up -d db_test
	@{ \
        make test-run; \
        EXIT_CODE=$$?; \
        make test-down; \
        exit 0; \
    }

test-e2e:
	@echo "-----| $(GREEN)Running e2e tests with selenium$(RESET) |-----"
	@echo "-----------------------------------------------"
	@docker-compose -f docker-compose.test.yml build
	@docker-compose -f docker-compose.test.yml up -d db_test
	@docker-compose -f docker-compose.test.yml up -d app_test

	@pytest tests/e2e/
	@echo "-----| $(RED)Tearing down e2e test suite$(RESET) |-----"
	@docker-compose -f docker-compose.test.yml down -v

test-run:
	@echo "-----| $(GREEN)Running tests with pytest$(RESET) |-----"
	@echo "-----------------------------------------------"
	@pytest backend/tests

test-down:
	@echo "-----| $(RED)Tearing down test suite$(RESET) |-----"
	@docker-compose -f docker-compose.test.yml down -v
	@echo "---------------------------------------------"
	@echo "-----| $(GREEN)Finished!$(RESET) |-----"

dev: build
	@echo "-----| $(GREEN)Starting containers in dev mode$(RESET) |-----"
	@docker-compose up -d dev_db
	@docker-compose up app

down:
	@docker-compose down

build:
	@echo "-----| $(GREEN)Building meal planner$(RESET) |-----"
	@docker-compose build --no-cache

clean:
	@echo "-----| $(RED)Removing meal planner and wiping database$(RESET) |-----"
	@read -p "⚠️ $(RED) Are you sure you want to permanently delete the DB? $(RESET)(y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "🗑️ $(YELLOW) Removing containers and database volumes...  $(RESET)"; \
		docker-compose down -v
		echo "🗑️ $(GREEN) Containers and database volumes removed succesfully   $(RESET)"; \
	else \
		echo "❌ $(GREEN)Aborted. Containers and volumes remain intact.$(RESET)"; \
	fi

re: down build dev
