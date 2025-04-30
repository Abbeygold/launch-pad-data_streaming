##################################################################################
#
# Makefile to build the project
#
#################################################################################

.PHONY: install venv lint format security test clean

# Create a virtual environment if not exists
venv:
	@test -d venv || python3 -m venv venv
	@echo "✅ Virtual environment ready."

# Install dependencies inside venv
install: venv
	. venv/bin/activate && pip install -r requirements.txt && pip install -r requirements-dev.txt

# Lint the project using flake8
lint:
	. venv/bin/activate && flake8 src tests --max-line-length=88

# Format the code using black
format:
	. venv/bin/activate && black src tests

# Run security checks using bandit
security:
	. venv/bin/activate && bandit -r src

# Run tests with pytest
test:
	. venv/bin/activate && pytest --maxfail=1 --disable-warnings -q

# Clean up .pyc files and other temporary files
clean:
	find . -name "*.pyc" -exec rm -f {} \;
