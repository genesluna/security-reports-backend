run:
		python manage.py runserver

migrate:
		python manage.py migrate

makemigrations:
		python manage.py makemigrations

sort:
		isort .

format:
		black .

lint:
		flake8 .

test:
		pytest

test_cov:
		coverage run -m pytest && coverage report -m

tree:
		tree -I __pycache__ > tree.txt   

requirements:
		pip freeze > requirements.txt
