start:
	docker-compose up
start-log-web:
	docker-compose up -d
	docker-compose logs -f www
migrate:
	docker-compose up flyway
ssh:
	docker-compose exec www bash
add:
	docker-compose exec www mmp install $(package)	
