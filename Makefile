
APP         := lsas
PYTHON      := .venv/bin/python
PYINSTALLER := .venv/bin/pyinstaller
BUILD_DIR   := lsas_build

.PHONY: deps-python build clean clean-old venv help

help:
	@echo "make deps-python # Python deps into venv"
	@echo "make build       # build binary"
	@echo "make clean"

venv: 
	python3 -m venv .venv

deps-python: venv
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements.txt

build: src/main.py | deps-python
	if [ -d $(BUILD_DIR) ]; then \
		rm -rf $(BUILD_DIR); \
	fi
	$(PYTHON) ./src/visuals/ui/compile_ui.py
	$(PYINSTALLER) --noconfirm --clean --onedir --name $(APP) $<
	mv dist/lsas $(BUILD_DIR)
	make clean

clean:
	rm -rf dist build .venv lsas.spec
