# League Scrim Analytics Suite

## Prerequisite

For loading the GUI it is mandatory, that one initializes a 
virtual environment, using the `requirements.txt`.

## Roadmap
Highest Priority (ordered)
- [x] Test on Patch 16.24
- [ ] Frontend für Datenauslese bzw. Visualisierung
- [x] Setup script für DB/Folder Struct {...} für Win/Linux
- [ ] Refactor globals/utils and read team_metadata from .conf file
    - [ ] Example .conf files (DB, team ...)
    
Low Prio // QOL:
- [x] Automate getting Patchname (Maybe Webscrape ?)
- [ ] Queries preparen für Frontend (kann warten bzw. geht schnell // improv.)
- [ ] Pipeline für Imports (bspw. per Owncloud oder Mail)
- [x] Proper Logging for DB-Transactions , Imports and file-moving with following convention:
``` [DD-MM-YYYY HH:MM:SS],[LOGLEVEL], MESSAGE ```
