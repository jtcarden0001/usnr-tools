# test
test:
	docker build -t test-image -f ./tools/docker/test.Dockerfile .
	docker run --env-file ./tools/docker/dev.env test-image

# run
dev-up:
	docker compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env up --build -d
	
dev-down:
	docker-compose -f ./tools/docker/dev.compose.yaml --env-file ./tools/docker/dev.env down -v