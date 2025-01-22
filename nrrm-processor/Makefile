# test
test:
	docker compose -f ./tools/docker/compose.yaml --project-name test --env-file ./tools/docker/test.env up --build

test-clean:
	docker stop test-nrrmprocessor
	docker rm test-nrrmprocessor
	docker stop test-nrrm-db
	docker rm test-nrrm-db
	docker volume rm test_nrrm_db_data

# run
prod-up:
	docker compose -f ./tools/docker/compose.yaml --project-name prod --env-file ./tools/docker/prod.env up --build

dev-up:
	docker compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env up --build -d
	
dev-down:
	docker-compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env down -v