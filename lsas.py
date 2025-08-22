from src.map import mapId
from src.data import loadDatabase

patch = "15.16.1" #TODO: Get from Matchdata

print(mapId(84  , patch, 'champion' ))
print(mapId(1042, patch, 'item'     ))
print(mapId(8100, patch, 'perk'     ))
print(mapId(4   , patch, 'summoner' ))

loadDatabase(patch, 'perk')
# testchange 

