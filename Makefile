CONFIG=./pyproject.toml

test:
	python -m unittest -v

format:
	black --config $(CONFIG) ./

static-analysis:
	mypy --config-file $(CONFIG) ./