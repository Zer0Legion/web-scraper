auto_fix:
	ruff check --fix

check:
	auto_fix
	poetry run pyright ./stockly/backend