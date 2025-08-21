import src.map as idmaps

patch = "15.16.1" #TODO: Get from Matchdata
url_pre              = 'https://ddragon.leagueoflegends.com/cdn/' + patch
mirror_champions_url =  url_pre + '/data/en_US/champion.json'
mirror_items_url     =  url_pre + '/data/en_US/item.json'
mirror_perks_url     =  url_pre + '/data/en_US/runesReforged.json'
mirror_summoner_url =  url_pre + '/data/en_US/summoner.json'

print(idmaps.toChampion(84, mirror_champions_url))
print(idmaps.toItem(1042, mirror_items_url))
print(idmaps.toPerk(8100, mirror_perks_url))
print(idmaps.toSummoner(4, mirror_summoner_url))


# testchange 

