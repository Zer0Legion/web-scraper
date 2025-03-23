auto_fix:
	ruff format
	ruff check --fix

check:
	make auto_fix
	poetry run pyright

dev:
	poetry run fastapi dev main.py

deploy:
	grep -oP '^ *"[^"]+"' pyproject.toml | sed 's/"//g' | sed 's/ (\([^)]*\))/>=\1/' > requirements.txt && python3 -c "with open('requirements.txt', 'r+') as f: data = f.read().replace('>=>=', '>='); f.seek(0); f.write(data); f.truncate()"
	vercel