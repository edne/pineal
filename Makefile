all: test style


test:
	nosetests -v --with-coverage --cover-erase --cover-package=pineal,tools


style:
	pep8 --exclude thirdparty .
	! grep -r --include \*.hy  '.\{61\}'
	cloc --force-lang=clojure,hy --exclude-dir=thirdparty .
