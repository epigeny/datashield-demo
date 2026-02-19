install:
	uv sync

update:
	rm uv.lock
	uv sync

run-utils:
	uv run python ds-utils.py

run-summaries:
	uv run python ds-summaries.py