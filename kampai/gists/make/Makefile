
# - - - - - - - - - - - - - - - - - - - - - - - -
# Tests

tests: pylint pytest

pylint:
	find . -iname "*.py" -not -path "./tests/*" | xargs pylint --output-format=colorized; true

pytest:
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

# - - - - - - - - - - - - - - - - - - - - - - - -
# Packages

install_requirements:
	pip install -r requirements.txt

install_project:
	pip install .

install_project_dev_mode:
	pip install -e .
