# Makefile

.PHONY: install-dev lint format security test clean all

# Install all dependencies including dev tools
install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Lint the project using flake8
lint:
	flake8 src tests --max-line-length=88

# Format the code using black
format:
	black src tests

# Run security checks using bandit
security:
	bandit -r src

# Run tests with pytest
test:
	pytest --maxfail=1 --disable-warnings -q

# Clean up .pyc files and other temporary files
clean:
	find . -type f -name "*.pyc" -delete

# Run all checks (formatting skipped to avoid auto changes)
all: lint security test