GREEN = $$(printf '\033[0;32m')
YELLOW = $$(printf '\033[0;33m')
RED = $$(printf '\033[0;31m')
RESET = $$(printf '\033[0m')

all: build

logs:
	@docker logs meal_planner_app_1

build:
	@echo "-----| $(GREEN)Building meal planner$(RESET) |-----"
	@docker-compose build --no-cache
	@docker-compose up -d

clean:
	@echo "-----| $(RED)Removing meal planner$(RESET) |-----"
	@docker-compose down

re: clean build
