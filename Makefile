PROJECT=emailhw
PYTHON_BIN=/usr/local/bin/python3
VIRTUALENV = ~/.virtualenvs/$(PROJECT)-venv
TESTCMD=nose2

all : test

.PHONY: test install package upload devinstall docbuild editor-tools doc-tools venv

test: venv
	. $(VIRTUALENV)/bin/activate && \
	$(TESTCMD)

install:
	$(PYTHON_BIN) setup.py --user install

clean:
	rm -fr build
	rm -fr dist
	rm -fr *.egg-info
	rm -fr docs/_build
	find . -name '*.pyc' -delete
	find . -name 'flycheck*.py' -delete
	find . -name '__pycache__' -delete

package: clean
	$(PYTHON_BIN) setup.py sdist bdist_wheel

upload: package
	twine upload dist/*



#
# Develop
# 
devinstall: venv
	. $(VIRTUALENV)/bin/activate && \
	python setup.py install

docbuild: devinstall
	. $(VIRTUALENV)/bin/activate && \
	sphinx-apidoc -o docs cnfformula && \
	$(MAKE) -C docs html

#
# Install tools
#
editor-tools : venv
	. $(VIRTUALENV)/bin/activate && \
	pip install pylint nose nose2

doc-tools : venv
	. $(VIRTUALENV)/bin/activate && \
	pip install sphinx sphinx-autobuild numpydoc sphinx_rtd_theme


#
# virtualenv setup
#
venv: $(VIRTUALENV)/bin/activate

$(VIRTUALENV)/bin/activate: requirements.txt
	type pip >/dev/null || easy_install --user pip
	type virtualenv>/dev/null || easy_install --user virtualenv
	test -d $(VIRTUALENV) || virtualenv -p $(PYTHON_BIN) $(VIRTUALENV)
	. $@ && pip install -Ur requirements.txt
	touch $@

