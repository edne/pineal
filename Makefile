all: test style


test:
	nosetests -v --with-coverage --cover-erase --cover-package=pineal,tools


style:
	flake8 --exclude thirdparty,tests,tools/__init__.py .
	! grep -r --include \*.hy  '.\{61\}'
	cloc --force-lang=clojure,hy --exclude-dir=thirdparty,examples .
