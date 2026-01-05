# League Scrim Analytics Suite

## Installing LSAS

For using `lsas`, one can use the `Makefile`:

```
make build
```

Then there will be a binary build in the `lsas_build` directory. Currently only Linux systems are supported.

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
