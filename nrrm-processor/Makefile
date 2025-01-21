# test
test:
	docker compose -f ./tools/docker/test.compose.yaml --project-name test --env-file ./tools/docker/test.env up --build

test-clean:
	docker stop test-nrrmprocessor
	docker rm test-nrrmprocessor
	docker stop dev-nrrmdata-db
	docker rm dev-nrrmdata-db
	docker volume rm docker_dev-db-data

# run
dev-up:
	docker compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env up --build -d
	
dev-down:
	docker-compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env down -v