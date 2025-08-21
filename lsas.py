import src.map as idmaps

patch = "15.16.1" #TODO: Get from Matchdata

mirror_champions_url = 'https://ddragon.leagueoflegends.com/cdn/' + patch + '/data/en_US/champion.json'
mirror_items_url     = 'https://ddragon.leagueoflegends.com/cdn/' + patch + '/data/en_US/item.json'
mirror_perks_url     = 'https://ddragon.leagueoflegends.com/cdn/' + patch + '/data/en_US/runesReforged.json'

#print(idmaps.toChampion(84, mirror_champions_url))
#print(idmaps.toItem(1042, mirror_items_url))
print(idmaps.toPerk(8100, mirror_perks_url))
# testchange 

