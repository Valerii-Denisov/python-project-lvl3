page-loader:
	poetry run page-loader

install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

upgrade:
	python3 -m pip uninstall hexlet-code
	poetry build
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest --basetemp=mydir -vv

test-cover:
	poetry run pytest --cov=page-loader tests --cov-report xml