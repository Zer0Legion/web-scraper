auto_fix:
	ruff format
	ruff check --fix

check:
	make auto_fix
	poetry run pyright

dev:
	poetry run fastapi dev main.py