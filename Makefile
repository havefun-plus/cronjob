isort:
	isort -rc .	

lint:
	flake8 --format=pylint --count --exit-zero cronjob tests examples

clean:
	find . -iname "*__pycache__" | xargs rm -rf
	find . -iname "*.pyc" | xargs rm -rf

test:
	PYTHONPATH=. pytest -s -vvvv --cov sspider --cov tests --cov-report term-missing --cov-report xml:cobertura.xml --junitxml=testresult.xml .


