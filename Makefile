run: SHELL:=/bin/bash
run:
	export PYTHONPATH=. && source .env && python -m core.receiver

test:
	export PYTHONPATH=. && pytest && flake8 . && mypy .
