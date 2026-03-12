# Use uv for all Python/package commands. Override with: make UV=python to use system Python.
UV = uv run

all: test

uninstall:
	uv pip uninstall openfisca-tunisia-pension -y 2>/dev/null || true

clean:
	rm -rf build dist
	find . -name '*.pyc' -exec rm \{\} \;

deps:
	uv pip install build twine

install:
	@# Install OpenFisca-Tunisia-Pension for development (editable).
	uv sync --extra dev

build: clean deps
	@# Build and install the package from wheel to test the distributed version.
	uv build
	uv pip uninstall openfisca-tunisia-pension -y 2>/dev/null || true
	find dist -name "*.whl" -exec uv pip install {}[dev] \;

check-syntax-errors:
	$(UV) python -m compileall -q .

check-style:
	$(UV) flake8 openfisca_tunisia_pension
	$(UV) flake8 tests

check-path-length:
	$(UV) python openfisca_tunisia_pension/scripts/check_path_length.py

check-yaml:
	.github/lint-changed-yaml-tests.sh

check-all-yaml:
	$(UV) yamllint openfisca_tunisia_pension/parameters
	$(UV) yamllint tests

test: clean check-syntax-errors check-style
	@echo "> YAML tests..."
	$(UV) openfisca test --country-package openfisca_tunisia_pension tests
