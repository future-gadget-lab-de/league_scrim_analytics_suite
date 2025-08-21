import src.map as idmaps

mirror_champions = 'https://ddragon.leagueoflegends.com/cdn/15.16.1/data/en_US/champion.json'
mirror_items     = 'https://ddragon.leagueoflegends.com/cdn/15.16.1/data/en_US/item.json'

print(idmaps.toChampion(84, mirror_champions))
print(idmaps.toItem(1042, mirror_items))

# testchange 