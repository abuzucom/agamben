.PHONY: sync check test

sync:
	python scripts/sync.py

check:
	python scripts/sync.py --check

test:
	python -m unittest discover -s tests -v
