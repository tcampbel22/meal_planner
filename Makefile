GREEN = $$(printf '\033[0;32m')
YELLOW = $$(printf '\033[0;33m')
RED = $$(printf '\033[0;31m')
RESET = $$(printf '\033[0m')

all: build

logs:
	@docker logs mealwise_dev

test-set-up:
	@echo "-----| $(GREEN)Starting containers in test mode$(RESET) |-----"
	@docker-compose -f docker-compose.test.yml up -d db

test-run:
	@echo "-----| $(GREEN)Running tests with pytest$(RESET) |-----"
	@echo "-----------------------------------------------"
	@pytest backend/tests

test-down:
	@echo "-----| $(RED)Tearing down test suite$(RESET) |-----"
	@docker-compose -f docker-compose.test.yml down -v
	@echo "---------------------------------------------"
	@echo "-----| $(GREEN)Finished!$(RESET) |-----"

test: test-set-up test-run test-down

dev:
	@echo "-----| $(GREEN)Starting containers in dev mode$(RESET) |-----"
	@docker-compose up -d dev_db
	@docker-compose up app

down:
	@docker-compose down

build:
	@echo "-----| $(GREEN)Building meal planner$(RESET) |-----"
	@docker-compose build --no-cache

clean:
	@echo "-----| $(RED)Removing meal planner$(RESET) |-----"
	@docker-compose down

re: clean build dev
