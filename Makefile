run: SHELL:=/bin/bash
run:
	PYTHONPATH=. && source .env && python core/receiver.py