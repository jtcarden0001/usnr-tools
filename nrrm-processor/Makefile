# test
test:
	docker compose -f ./tools/docker/test.compose.yaml --env-file ./tools/docker/dev.env up --build -d

# run
dev-up:
	docker compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env up --build -d
	
dev-down:
	docker-compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env down -v