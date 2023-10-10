newdb:
	docker-compose stop api
	docker-compose exec postgres psql -h postgres -U postgres -c "drop database boilerplate;"
	docker-compose exec postgres psql -h postgres -U postgres -c "create database boilerplate;"
	docker-compose start api

newmi:
	docker-compose run --rm api boilerplate/manage.py makemigrations payments accounts

mi:
	docker-compose run --rm api boilerplate/manage.py migrate

newu:
	docker-compose exec -e DJANGO_SUPERUSER_PASSWORD=123 api boilerplate/manage.py createsuperuser --username yuri --email yuri@yuri.com --no-input

delmi:
	docker-compose run --rm api rm -rf boilerplate/payments/migrations boilerplate/accounts/migrations boilerplate/products/migrations

reset: newdb delmi newmi mi newu
