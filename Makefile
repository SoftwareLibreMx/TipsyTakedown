start:
	docker compose up
start-log-web:
	docker compose up -d
	docker compose logs -f www
migrate:
	docker compose up flyway
ssh:
	docker compose exec www bash
autopep8:
	docker compose exec www autopep8 --in-place --aggressive --recursive /$(path)
autopep8-all:
	docker compose exec www autopep8 --in-place --aggressive --recursive .
add:
	docker compose exec www mmp install $(package)
test:
	docker compose exec www pytest /www
start-encoding-docker:
	docker compose up -d
	docker compose exec www python3 -c "from api.modules.video.application.encoder_application import process_video_queue; process_video_queue()"
start-encoding:
	python3 -c "from www.api.modules.video.application.encoder_application import process_video_queue; process_video_queue()"

