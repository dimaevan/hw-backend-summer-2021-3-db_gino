run:
	@python main.py
migrate:
	alembic upgrade head
firstmigration:
	alembic revision -m "first migrations" --autogenerate --head head