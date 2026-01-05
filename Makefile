
appname 	:= lsas
PYTHON 		:= .venv/bin/python
PYINSTALLER := .venv/bin/pyinstaller

.PHONY: deps-python build clean clean-old venv help

help:
	@echo "make deps-python     # Python deps into venv"
	@echo "make build       	# build binary"
	@echo "make clean"

venv: 
	python3 -m venv .venv

deps-python: venv
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements.txt

build: src/main.py | deps-python
	if [ -d lsas_build ]; then \
		rm -rf lsas_build; \
	fi
	$(PYTHON) ./src/visuals/ui/compile_ui.py
	$(PYINSTALLER) --noconfirm --clean --onedir --name $(appname) $<
	mv dist/lsas lsas_build
	make clean

clean:
	rm -rf dist build .venv lsas.spec
