run: SHELL:=/bin/bash
run:
	export PYTHONPATH=. && source .env && python core/receiver.py

test:
	export PYTHONPATH=. && pytest