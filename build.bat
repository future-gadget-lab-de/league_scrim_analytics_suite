set cus_pip=.\.venv\Scripts\pip.exe
set cus_py=.\.venv\Scripts\python.exe
set cus_install=.\.venv\Scripts\pyinstaller.exe
set APP=lsas
set build_dir=%APP%_build

python -m venv .venv
%cus_pip% install -r requirements.txt
%cus_py% .\src\visuals\ui\compile_ui.py

%cus_install% --noconfirm --clean --onedir --name %APP% .\src\main.py
MOVE .\dist\lsas .\%build_dir%
rmdir /s /q .\dist
rmdir /s /q .\.venv
rmdir /s /q .\build
rmdir /s /q .\lsas.spec
