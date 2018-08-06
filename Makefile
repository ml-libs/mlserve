# Some simple testing tasks (sorry, UNIX only).

FLAGS=

flake: checkrst bandit
	flake8 mlserve tests examples setup.py demos

test: flake
	py.test -s -v $(FLAGS) ./tests/

vtest:
	py.test -s -v $(FLAGS) ./tests/

checkrst:
	python setup.py check --restructuredtext

bandit:
	bandit -r ./mlserve

pyroma:
	pyroma -d .

mypy:
	mypy mlserve --ignore-missing-imports --disallow-untyped-calls --no-site-packages --strict

testloop:
	while true ; do \
        py.test -s -v $(FLAGS) ./tests/ ; \
    done

cov cover coverage: flake checkrst
	py.test -s -v --cov-report term --cov-report html --cov mlserve ./tests
	@echo "open file://`pwd`/htmlcov/index.html"

cov_only:
	py.test -s -v --cov-report term --cov-report html --cov mlserve ./tests
	@echo "open file://`pwd`/htmlcov/index.html"

ci: flake mypy
	py.test -s -v --cov-report term --cov-report html --cov mlserve ./tests
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"

.PHONY: all flake test vtest cov clean doc ci
