# League Scrim Analytics Suite

## Installing LSAS

The first prerequisite is to install Python. In the Windows case, that is enough (see [Python Downloads for Windows](https://www.python.org/downloads/)), but in the Linux case there could be packages to install, too.

### Linux
One can use the `Makefile` to build the Program:

```
make build
```
and then use it under the `lsas_build` directory.

### Windows

Here one can just execute the provided `build.bat`. Then the build program should be in the directory `lsas_build` aswell.

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
