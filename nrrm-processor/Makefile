# test
test:
	docker compose -f ./tools/docker/test.compose.yaml --env-file ./tools/docker/dev.env up --build

test-clean:
	docker stop dev-nrrmdata-db
	docker rm dev-nrrmdata-db
	docker volume rm docker_dev-db-data
	docker rm test-nrrmprocessor

# run
dev-up:
	docker compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env up --build -d
	
dev-down:
	docker-compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env down -v