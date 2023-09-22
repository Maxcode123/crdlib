CONFIG=./pyproject.toml
TEST=python -m unittest -v
FORMATTER=black
TYPE_CHECKER=mypy

test: unit-test integration-test

unit-test:
	$(TEST) tests.unit

integration-test:
	$(TEST) tests.integration

format:
	$(FORMATTER) --config $(CONFIG) ./

static-analysis:
	$(TYPE_CHECKER) --config-file $(CONFIG) ./