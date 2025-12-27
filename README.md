# League Scrim Analytics Suite

## Prerequisite

To be functional, one must first compile the .ui files:

```
.../LSAS $ python3 -m ./src/visuals/ui/compile_ui.py
``` 

To successfully get this script working, one must check
- that pwd returns `/pathtoprojects/.../LSAS` (not in a literal sense)
- the virtual environment is installed in a the directory `.venv`

## Roadmap
Highest Priority (ordered)
- [x] Test on Patch 16.24
- [ ] Frontend für Datenauslese bzw. Visualisierung
- [ ] Setup script für DB/Folder Struct {...} für Win/Linux
- [ ] Refactor globals/utils and read team_metadata from .conf file
    - [ ] Example .conf files (DB, team ...)
    
Low Prio // QOL:
- [ ] Automate getting Patchname (Maybe Webscrape ?)
    - [ ] Automatisierte Merge-Request erstellung für Patch erneuerung (Renovate Bot)
- [ ] Queries preparen für Frontend (kann warten bzw. geht schnell // improv.)
- [ ] Pipeline für Imports (bspw. per Owncloud oder Mail)
- [ ] Proper Logging for DB-Transactions , Imports and file-moving with following convention:
``` [DD-MM-YYYY HH:MM:SS],[LOGLEVEL], MESSAGE ```
