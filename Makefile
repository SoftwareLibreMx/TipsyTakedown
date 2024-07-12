start:
	docker-compose up
start-log-web:
	docker-compose up -d
	docker-compose logs -f www
migrate:
	docker-compose up flyway
ssh:
	docker-compose exec www bash
autopep8:
	docker-compose exec www autopep8 --in-place --aggressive --recursive /$(path)
add:
	docker-compose exec www mmp install $(package)	
