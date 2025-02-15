poetry run flake8 --toml-config pyproject.toml
poetry run isort .
poetry run black --config pyproject.toml .

poetry run mypy src
poetry run mypy main.py
poetry run pylint --rcfile=pyproject.toml src
poetry run pylint --rcfile=pyproject.toml main.py

poetry run pytest